PImage oImage, tImage, mImage;
PVector mOrigin, mSize;

int ALPHA_THRESHOLD = 0xF0;
float DESIRED_RATIO = 3.0f;

String IMAGES_DIR = "../../../imgs";
String FULL_IMAGES_DIR = IMAGES_DIR + "/" + "00.Original";
String TRANSPARENT_IMAGES_DIR = IMAGES_DIR + "/" + "01.Background";
String OUTPUT_IMAGES_DIR = IMAGES_DIR + "/" + "02.Crop";

void setup() {
  size(10, 10);
  background(255);
  noLoop();

  //String fname = "MUMI-138-Tochilinita"; // JPG
  String fname = "MUMI-005-Hematita"; // CMKY

  if (args != null) {
    fname = args[0];
  }

  try {
    oImage = loadImage(dataPath(FULL_IMAGES_DIR + "/" + fname + ".jpg"));
  }
  catch(Exception jpgE) {
    try {
      oImage = loadImage(dataPath(FULL_IMAGES_DIR + "/" + fname + ".JPG"));
    }
    catch(Exception JPGe) {
      println("--- ERROR : Can't open " + fname + ".jpg");
      exit();
    }
  }

  tImage = loadImage(dataPath(TRANSPARENT_IMAGES_DIR + "/" + fname + ".png"));

  mOrigin = new PVector();
  mSize = new PVector();

  getNonTransparentRectangle(tImage, mOrigin, mSize);

  if (int(mSize.x * oImage.width) == 0 || int(mSize.y * oImage.height) == 0) {
    println("--- ERROR : got 0x0 crop from " + fname);
    exit();
  }


  mImage = createImage(int(mSize.x * oImage.width), int(mSize.y * oImage.height), RGB);

  mImage.copy(oImage, 
    int(mOrigin.x * oImage.width), int(mOrigin.y * oImage.height), 
    int(mSize.x * oImage.width), int(mSize.y * oImage.height), 
    0, 0, mImage.width, mImage.height);

  // TODO: min dimension to keep
  mImage.save(dataPath(OUTPUT_IMAGES_DIR + "/" + fname + ".jpg"));

  exit();
}

void draw() {
}


// https://stackoverflow.com/a/30418912
int getNonTransparentRectangle(PImage mask, PVector origin, PVector size) {
  int maskWidth = mask.width;
  int maskHeight = mask.height;

  int runningWidth[][] = new int[maskHeight][maskWidth];
  int runningHeight[][] = new int[maskHeight][maskWidth];

  int alphaThreshold = ALPHA_THRESHOLD;
  float desiredAspectRatio = DESIRED_RATIO;

  int maxArea = 0;

  for (int r = 0; r < maskHeight; r++) {
    for (int c = 0; c < maskWidth; c++) {
      int maskAlpha = ((mask.pixels[r * maskWidth + c] >> 24) & 0xFF) > alphaThreshold ? 0x01 : 0x00;

      if (maskAlpha == 0x00) continue;

      if (r == 0) runningHeight[r][c] = 1;
      else runningHeight[r][c] = runningHeight[r - 1][c] + 1;

      if (c == 0) runningWidth[r][c] = 1;
      else runningWidth[r][c] = runningWidth[r][c - 1] + 1;

      int minW = runningWidth[r][c];

      for (int dh = 0; dh < runningHeight[r][c]; dh++) {
        minW = min(minW, runningWidth[r - dh][c]);

        int mArea = (dh + 1) * minW;
        float mAspectRatio = (maskWidth >= maskHeight) ? float(minW) / float(dh + 1) : float(dh + 1) / float(minW);

        if (mArea > maxArea && mAspectRatio > desiredAspectRatio) {
          maxArea = mArea;

          origin.x = float(c - minW + 1) / float(maskWidth);
          origin.y = float(r - dh) / float(maskHeight);

          size.x = float(minW) / float(maskWidth);
          size.y = float(dh + 1) / float(maskHeight);
        }
      }
    }
  }

  return maxArea;
}

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
  //String fname = "MUMI-004-1-Hematita"; // vertical
  //String fname = "MUMI-004-2-Hematita"; // small

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

  int mImageWidth = (int)max(1, mSize.x * oImage.width);
  int mImageHeight = (int)max(1, mSize.y * oImage.height);

  mImage = createImage(mImageWidth, mImageHeight, RGB);

  mImage.copy(oImage, 
    int(mOrigin.x * oImage.width), int(mOrigin.y * oImage.height), 
    int(mSize.x * oImage.width), int(mSize.y * oImage.height), 
    0, 0, mImage.width, mImage.height);

  if ((mImage.width > 1000) || (mImage.height > 1000)) {
    mImage.save(dataPath(OUTPUT_IMAGES_DIR + "/" + fname + ".jpg"));
  } else {
    mImage.save(dataPath(OUTPUT_IMAGES_DIR + "/_x/" + fname + ".jpg"));
  }

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

  int[] maxArea = new int[int(DESIRED_RATIO)];
  float[] desiredAspectRatioValue = new float[maxArea.length];
  PVector[] maxOrigin = new PVector[maxArea.length];
  PVector[] maxSize = new PVector[maxArea.length];

  for (int i = 0; i < maxArea.length; i++) {
    maxArea[i] = 0;
    desiredAspectRatioValue[i] = DESIRED_RATIO - float(i);
    maxOrigin[i] = new PVector(0, 0, 0);
    maxSize[i] = new PVector(0, 0, 0);
  }

  for (int row = 0; row < maskHeight; row++) {
    for (int col = 0; col < maskWidth; col++) {
      int maskAlpha = ((mask.pixels[row * maskWidth + col] >> 24) & 0xFF) > alphaThreshold ? 0x01 : 0x00;

      if (maskAlpha == 0x00) continue;

      if (row == 0) runningHeight[row][col] = 1;
      else runningHeight[row][col] = runningHeight[row - 1][col] + 1;

      if (col == 0) runningWidth[row][col] = 1;
      else runningWidth[row][col] = runningWidth[row][col - 1] + 1;

      int minW = runningWidth[row][col];

      for (int dh = 0; dh < runningHeight[row][col]; dh++) {
        minW = min(minW, runningWidth[row - dh][col]);

        int mArea = (dh + 1) * minW;
        float mAspectRatio = (maskWidth >= maskHeight) ? float(minW) / float(dh + 1) : float(dh + 1) / float(minW);

        for (int aspectRatioIndex = 0; aspectRatioIndex < maxArea.length; aspectRatioIndex++) {
          if (mArea > maxArea[aspectRatioIndex] && mAspectRatio > desiredAspectRatioValue[aspectRatioIndex]) {
            maxArea[aspectRatioIndex] = mArea;

            maxOrigin[aspectRatioIndex].x = float(col - minW + 1) / float(maskWidth);
            maxOrigin[aspectRatioIndex].y = float(row - dh) / float(maskHeight);

            maxSize[aspectRatioIndex].x = float(minW) / float(maskWidth);
            maxSize[aspectRatioIndex].y = float(dh + 1) / float(maskHeight);
          }
        }
      }
    }
  }

  for (int aspectRatioIndex = 0; aspectRatioIndex < maxArea.length; aspectRatioIndex++) {
    if (maxArea[aspectRatioIndex] > 0) {
      origin.set(maxOrigin[aspectRatioIndex]);
      size.set(maxSize[aspectRatioIndex]);
      return maxArea[aspectRatioIndex];
    }
  }

  return 0;
}

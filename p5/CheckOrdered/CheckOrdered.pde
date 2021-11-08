String BY = "hls";

void setup() {
  size(128, 128);
  noLoop();

  JSONArray json;
  PGraphics allImages;

  allImages = createGraphics(192, 63 * 1000);

  json = loadJSONArray("../../imgs/06.Ordered/by_" + BY + ".json");
  println(json.size());

  allImages.beginDraw(); 
  for (int i = 0; i < 1000; i++) {
    String filename = json.getString(i);
    if (i%100==0)
      println(i + " : " + filename);

    PImage mImage = loadImage("../../imgs/04.Sized/" + filename + ".jpg");
    mImage.resize(192, 63);
    allImages.image(mImage, 0, i * 63);
  }
  allImages.endDraw();
  allImages.save(BY + "_1000.jpg");

  allImages.beginDraw(); 
  for (int i = 0; i < 1000; i++) {
    int ii = i + 1000;

    String filename = json.getString(ii);
    if (ii%100==0)
      println(ii + " : " + filename);

    PImage mImage = loadImage("../../imgs/04.Sized/" + filename + ".jpg");
    mImage.resize(192, 63);
    allImages.image(mImage, 0, i * 63);
  }
  allImages.endDraw();
  allImages.save(BY + "_2000.jpg");
  
  exit();
}

void draw() {
}

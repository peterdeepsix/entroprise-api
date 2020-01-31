"use strict";

// [START run_imageproc_handler_setup]
const gm = require("gm").subClass({ imageMagick: true });
const fs = require("fs");
const { promisify } = require("util");
const path = require("path");
const vision = require("@google-cloud/vision");

const { Storage } = require("@google-cloud/storage");
const storage = new Storage();
const client = new vision.ImageAnnotatorClient();

const { BLURRED_BUCKET_NAME } = process.env;

exports.blurOffensiveImages = async event => {
  const object = event;

  const file = storage.bucket(object.bucket).file(object.name);
  const filePath = `gs://${object.bucket}/${object.name}`;

  console.log(`Analyzing ${file.name}.`);

  try {
    const [result] = await client.webDetection(filePath);
    const detections = result.webEntities || {};
    console.log(detections);
    if (
      // https://cloud.google.com/vision/docs/reference/rest/v1/AnnotateImageResponse#likelihood
      detections.adult === "VERY_LIKELY" ||
      detections.violence === "VERY_LIKELY"
    ) {
      console.log(`Detected ${file.name} as inappropriate.`);
      return blurImage(file, BLURRED_BUCKET_NAME);
    } else {
      console.log(`Detected ${file.name} as OK.`);
      return blurImage(file, BLURRED_BUCKET_NAME);
    }
  } catch (err) {
    console.error(`Failed to analyze ${file.name}.`, err);
    throw err;
  }
};

const blurImage = async (file, blurredBucketName) => {
  const tempLocalPath = `/tmp/${path.parse(file.name).base}`;

  try {
    await file.download({ destination: tempLocalPath });

    console.log(`Downloaded ${file.name} to ${tempLocalPath}.`);
  } catch (err) {
    throw new Error(`File download failed: ${err}`);
  }

  await new Promise((resolve, reject) => {
    gm(tempLocalPath)
      .blur(0, 16)
      .write(tempLocalPath, (err, stdout) => {
        if (err) {
          console.error("Failed to blur image.", err);
          reject(err);
        } else {
          console.log(`Blurred image: ${file.name}`);
          resolve(stdout);
        }
      });
  });

  const blurredBucket = storage.bucket(blurredBucketName);

  const gcsPath = `gs://${blurredBucketName}/${file.name}`;
  try {
    await blurredBucket.upload(tempLocalPath, { destination: file.name });
    console.log(`Uploaded blurred image to: ${gcsPath}`);
  } catch (err) {
    throw new Error(`Unable to upload blurred image to ${gcsPath}: ${err}`);
  }

  const unlink = promisify(fs.unlink);
  return unlink(tempLocalPath);
};

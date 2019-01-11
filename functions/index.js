const functions = require('firebase-functions');
const Video = require('@google-cloud/video-intelligence').v1p2beta1;
var admin = require("firebase-admin");

admin.initializeApp(functions.config().firebase);

exports.helloWorld = functions.https.onRequest((request, response) => {
 response.send("Hello from Firebase!");
});

exports.processVideo = functions.https.onRequest(async function (_request, response) {
	console.log('Beginning video process...');
  	const video = new Video.VideoIntelligenceServiceClient();

 	const gcsUri = 'gs://mta-bus-view.appspot.com/MTA-Bus-Sample-Video.mp4';

 	const request = {
 	  inputUri: gcsUri,
 	  features: ['OBJECT_TRACKING'],
 	  //recommended to use us-east1 for the best latency due to different types of processors used in this region and others
 	  locationId: 'us-east1',
 	};

 	console.log('Waiting for operation to complete...');

 	// Detects objects in a video
 	const [operation] = await video.annotateVideo(request);
 	const results = await operation.promise();
 	console.log(results);

 	//Gets annotations for video
 	const annotations = results[0].annotationResults[0];
 	

 	// response.send("Attempting to process the video! \n\n", JSON.stringify(results, null, 2));
});

const processVideo = (req, res) => {

}

const logResults = (results) => {

	const objects = annotations.objectAnnotations;
 	objects.forEach(object => {
 	  console.log(`Entity description:  ${object.entity.description}`);
 	  console.log(`Entity id: ${object.entity.entityId}`);
 	  const time = object.segment;
 	  if (time.startTimeOffset.seconds === undefined) {
 	    time.startTimeOffset.seconds = 0;
 	  }
 	  if (time.startTimeOffset.nanos === undefined) {
 	    time.startTimeOffset.nanos = 0;
 	  }
 	  if (time.endTimeOffset.seconds === undefined) {
 	    time.endTimeOffset.seconds = 0;
 	  }
 	  if (time.endTimeOffset.nanos === undefined) {
 	    time.endTimeOffset.nanos = 0;
 	  }
 	  console.log(
 	    `Segment: ${time.startTimeOffset.seconds}` +
 	      `.${(time.startTimeOffset.nanos / 1e6).toFixed(0)}s to ${
 	        time.endTimeOffset.seconds
 	      }.` +
 	      `${(time.endTimeOffset.nanos / 1e6).toFixed(0)}s`
 	  );
 	  console.log(`Confidence: ${object.confidence}`);
 	  const frame = object.frames[0];
 	  const box = frame.normalizedBoundingBox;
 	  const timeOffset = frame.timeOffset;
 	  if (timeOffset.seconds === undefined) {
 	    timeOffset.seconds = 0;
 	  }
 	  if (timeOffset.nanos === undefined) {
 	    timeOffset.nanos = 0;
 	  }
 	  console.log(
 	    `Time offset for the first frame: ${timeOffset.seconds}` +
 	      `.${(timeOffset.nanos / 1e6).toFixed(0)}s`
 	  );
 	  console.log(`Bounding box position:`);
 	  console.log(`\tleft   :${box.left}`);
 	  console.log(`\ttop    :${box.top}`);
 	  console.log(`\tright  :${box.right}`);
 	  console.log(`\tbottom :${box.bottom}`);
 	});
}


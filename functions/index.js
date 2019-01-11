const functions = require('firebase-functions');
const Video = require('@google-cloud/video-intelligence').v1p2beta1;
var admin = require("firebase-admin");

admin.initializeApp(functions.config().firebase);

exports.processVideo = functions.https.onRequest(async function (_request, response) {
	console.log('Beginning video process...');
  	const video = new Video.VideoIntelligenceServiceClient();

 	const gcsUri = 'gs://mta-bus-view.appspot.com/MTA-Bus-Sample-Video.mp4';

 	const request = {
 	  inputUri: gcsUri,
 	  features: ['OBJECT_TRACKING'],
 	  locationId: 'us-east1',
 	};

 	console.log('Waiting for operation to complete...');

 	// Detects objects in a video
 	const [operation] = await video.annotateVideo(request);
 	const results = await operation.promise();

 	//Gets annotations for video
 	const annotations = results[0].annotationResults[0];
 	
 	saveResultsToDatabase(annotations);

 	response.send("Attempting to process the video!");
});

const saveResultsToDatabase = (annotations) => {
	admin.database().ref('results').set(annotations);
					
}



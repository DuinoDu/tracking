#include <opencv2/core/utility.hpp>
#include <opencv2/tracking.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <cstring>

using namespace std;
using namespace cv;

static Mat image;
static Rect2d boundingBox;
static bool paused;
static bool selectObject = false;
static bool startSelection = false;

int main( int argc, char** argv ){

  String tracker_algorithm = "KCF"; //parser.get<String>( 0 );

  boundingBox.x = 220;
  boundingBox.y = 180;
  boundingBox.width = 80;
  boundingBox.height = 80;

  VideoCapture cap;
  if (argc == 2)
    cap.open( argv[1] );
  else 
    cap.open( 0 );

  if( !cap.isOpened() )
  {
    cout << "***Could not initialize capturing...***\n";
    cout << "Current parameter's value: \n";
    return -1;
  }

  Mat frame;
  paused = true;
  namedWindow( "Tracking API", 1 );

  //instantiates TrackerKCF
  Ptr<TrackerKCF> tracker = TrackerKCF::createTracker(); 
  tracker->setROI(2,5);
  if( tracker == NULL )
  {
    cout << "***Error in the instantiation of the tracker...***\n";
    return -1;
  }

  bool initialized = false;
  int frameCounter = 0;

  for ( ;; )
  {
    cap >> frame;

    if( !initialized )
    {
      //initializes the tracker
      if( !tracker->init( frame, boundingBox ) )
      {
        cout << "***Could not initialize tracker...***\n";
        return -1;
      }
      initialized = true;
    }
    else if( initialized )
    {
      //updates the tracker
      if( tracker->update( frame, boundingBox ) )
      {
        rectangle( frame, boundingBox, Scalar( 255, 0, 0 ), 2, 1 );
      }
    }
    imshow( "Tracking API", frame );
    frameCounter++;

    char c = (char) waitKey( 2 );
    if( c == 'q' )
      break;
  }
  return 0;
}

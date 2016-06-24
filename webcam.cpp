#include <iostream>
#include <python2.7/Python.h>

using namespace std;


int main(int argc, char *argv[]){
cout<< "Hello World!";

  Py_SetProgramName(argv[0]);  /* optional but recommended */
  Py_Initialize();
  PyRun_SimpleString("from time import time,ctime\n"
                     "print 'Today is',ctime(time())\n");
  Py_Finalize();

//made changes
return 0;
}

## BuildIt Installation
<hr>
The following section documents the steps to fetch, compile and run test cases for the BuildIt library. The library is available open-source under the MIT license.

### Requirements
BuildIt is a light-weight C++ library and doesn't require any special compiler. The main requirements are -

- Linux/MacOS platform
- C++ and C Compiler (C++11 compliant)
- make (GNU Make)
- git

### Cloning and Building
Start by cloning the main BuildIt repo with the command -

	git clone --recursive https://github.com/BuildIt-lang/buildit.git

To build the repository, navigate to the directory and run make

	make -j $(nproc)

If no errors are reported, you can run the samples that also double and test cases with the command -

	make run

The build system should run all the test cases and report if any fail.


### Using BuildIt in your project
Once you have successfully built BuildIt from source, you are ready to start using it in your project. You just need to notedown the path where you had cloned BuildIt in the previous section. We will need the path to the tell the compiler where the headers and libraries are. The officially supported way to obtain the correct compile and link flags is to use the `compile-flags` and `linker-flags` targets from the Makefile. Suppose you write a C++ file foo.cpp that uses BuildIt types and functions, you can compile it as -

	g++ $(make --no-print-directory -C <path-to-buildit-rep> compile-flags) foo.cpp $(make --no-print-directory -C <path-to-buildit-repo> linker-flags) -O3 -o foo


###Using the online tool
The following section documents using the online tool available on the BuildIt website which is a great way to try BuildIt without having to download and install it.

Start by navigating to the online tool at [https://buildit.so/tryit](https://buildit.so/tryit). You will be presented with a popup that lists several samples and a disclaimer about use of the online tool. You can choose one of the samples by clicking on the link and dismiss the popup with the close button. At any time, the popup can be brought up again by clicking the ? button in the top menu bar. 

Write/Edit the code in the main text area as you would in a cpp file. The language spec for the online tool is exactly the same except for a few restrictions -

1. Since the compiled code runs on our web-servers, we have restricted access to the file system and other systemcalls. If you perform any restricted systemcall (Eg. open), you will be presented with the Bad System Call error message.
2. For similar reasons as above, we have restricted the code execution time to 5 seconds and some limits on the amount of memory that can be used by the process. Please try to keep the programs small and simple.

After writing the code you can hit the triangle shaped run button in the top menu bar. The tool will build and execute your code and add another stage in the top menu bar (next to Stage 1). You will also automatically be navigated to the newly generated stage. You can navigate between the stages by clicking on the appropriate stage. You can further modify the code generated for the second stage and execute it as before with the run button. In case your program encounters an error either during compilation or execution, the error message would be shown in the newly added stage in red. 

To share a code snippet, click on the share button in the top menu bar (left of the triangular run button) and a small popup will present a unique link for the currently opened stage code. You can copy and share this link. Please remember that the shared link is only for the current stage and not for the previous stages or the next stages.

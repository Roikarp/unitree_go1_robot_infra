# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.26

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/user_108/.local/lib/python3.8/site-packages/cmake/data/bin/cmake

# The command to remove a file.
RM = /home/user_108/.local/lib/python3.8/site-packages/cmake/data/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/user_108/project_b/custom_agent

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/user_108/project_b/custom_agent/build

# Include any dependencies generated for this target.
include CMakeFiles/learning.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/learning.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/learning.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/learning.dir/flags.make

CMakeFiles/learning.dir/code/learning.cpp.o: CMakeFiles/learning.dir/flags.make
CMakeFiles/learning.dir/code/learning.cpp.o: /home/user_108/project_b/custom_agent/code/learning.cpp
CMakeFiles/learning.dir/code/learning.cpp.o: CMakeFiles/learning.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/user_108/project_b/custom_agent/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/learning.dir/code/learning.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/learning.dir/code/learning.cpp.o -MF CMakeFiles/learning.dir/code/learning.cpp.o.d -o CMakeFiles/learning.dir/code/learning.cpp.o -c /home/user_108/project_b/custom_agent/code/learning.cpp

CMakeFiles/learning.dir/code/learning.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/learning.dir/code/learning.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/user_108/project_b/custom_agent/code/learning.cpp > CMakeFiles/learning.dir/code/learning.cpp.i

CMakeFiles/learning.dir/code/learning.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/learning.dir/code/learning.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/user_108/project_b/custom_agent/code/learning.cpp -o CMakeFiles/learning.dir/code/learning.cpp.s

# Object files for target learning
learning_OBJECTS = \
"CMakeFiles/learning.dir/code/learning.cpp.o"

# External object files for target learning
learning_EXTERNAL_OBJECTS =

learning: CMakeFiles/learning.dir/code/learning.cpp.o
learning: CMakeFiles/learning.dir/build.make
learning: CMakeFiles/learning.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/user_108/project_b/custom_agent/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable learning"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/learning.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/learning.dir/build: learning
.PHONY : CMakeFiles/learning.dir/build

CMakeFiles/learning.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/learning.dir/cmake_clean.cmake
.PHONY : CMakeFiles/learning.dir/clean

CMakeFiles/learning.dir/depend:
	cd /home/user_108/project_b/custom_agent/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/user_108/project_b/custom_agent /home/user_108/project_b/custom_agent /home/user_108/project_b/custom_agent/build /home/user_108/project_b/custom_agent/build /home/user_108/project_b/custom_agent/build/CMakeFiles/learning.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/learning.dir/depend


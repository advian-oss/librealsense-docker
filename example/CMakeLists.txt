cmake_minimum_required(VERSION 3.1.0)
project(rs-reset)
add_executable(rs-reset src/main.cpp)
set_property(TARGET rs-reset PROPERTY CXX_STANDARD 11)

find_package(realsense2 REQUIRED)
target_include_directories(
        rs-reset
        PRIVATE
        ${realsense2_INCLUDE_DIR}
        )

target_link_libraries(
        rs-reset
        ${realsense2_LIBRARY}
        )

macro(print_all_variables)
        message(STATUS "print_all_variables------------------------------------------{")
        get_cmake_property(_variableNames VARIABLES)
        foreach (_variableName ${_variableNames})
                message(STATUS "${_variableName}=${${_variableName}}")
        endforeach()
        message(STATUS "print_all_variables------------------------------------------}")
endmacro()
print_all_variables()

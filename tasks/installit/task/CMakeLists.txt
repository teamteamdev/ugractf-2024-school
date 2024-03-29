cmake_minimum_required(VERSION 3.27)

project(install_it)

file(GLOB common_src "src/*.c")
add_compile_options(-Wall -Werror -std=c11 -Wpedantic)
include_directories(./include)

add_executable(install_it install_it.c ${common_src})
target_link_libraries(install_it PRIVATE "-static" "-flto" "-s")

add_executable(patch_it patch_it.c ${common_src})

add_executable(fast_flag fast_flag.c ${common_src})

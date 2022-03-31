import argparse
import os
import argparse
import pathlib
from tabnanny import verbose
from PIL import Image as img
from alive_progress import alive_bar


all_args = argparse.ArgumentParser(
    description="Take images from folder and tile them to create a finished tile."
)

all_args.add_argument("-i", "--input", required=False, default=os.getcwd())
all_args.add_argument("-o", "--output", required=False)
all_args.add_argument("-g", "--grid", required=True)
all_args.add_argument("-v", "--verbose", required=False)
args_in = vars(all_args.parse_args())


if args_in["verbose"] is not None:
    verbose = True
    print("Running in verbose mode.")
    print("Inputs: " + str(args_in))


output = args_in["output"]
if output is None:
    output = args_in["input"]
if pathlib.Path(output).suffix == "":
    output = output + "output.jpg"

if verbose == True:
    print("Output set to: " + output)


grid = args_in["grid"].split("x")
grid[0] = int(grid[0])
grid[1] = int(grid[1])

if verbose == True:
    print(grid)


files = []
for each in os.listdir(args_in["input"]):
    if pathlib.Path(str(args_in["input"]) + "\\" + each).suffix == ".png":
        files.append(each)
files.sort()

if verbose == True:
    print(str(files))


baseImage = img.open(str(args_in["input"]) + "\\" + files[0])
outputImage = img.new(
    mode="RGB",
    size=(
        baseImage.size[0] * grid[0],
        baseImage.size[1] * grid[1],
    ),
)

outputImage.save(str(output))

if verbose == True:
    print("Base image: " + str(baseImage.size))
    print("Output image: " + str(outputImage.size))


column = []
row = [(baseImage.size[1] * grid[1]) - baseImage.height]


with alive_bar(
    grid[0] * grid[1], title="Tiling...", bar="filling", spinner="wait"
) as bar:
    for each in files:
        workingImage = img.open(str(args_in["input"]) + "\\" + each)
        outputImage.paste(
            workingImage,
            (sum(column), sum(row)),
        ),

        if sum(row) == 0:
            row = [baseImage.size[1] * grid[1]]
            column.append(baseImage.height)

        outputImage.save(str(output))

        if verbose == True:
            print(sum(column), sum(row))
            print("Saved")

        row.append(-baseImage.height)
        if sum(column) == outputImage.width + baseImage.width:
            break

        bar()


print("Finished tile saved at: " + output)

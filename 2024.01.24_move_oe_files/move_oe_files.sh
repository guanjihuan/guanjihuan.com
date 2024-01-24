if [ ! -d "./trash" ]; then
        mkdir ./trash
fi

mv *.o* ./trash
mv *.e* ./trash
# EndGame


## Installation

Use your local machine 

OR

Use the docker to run the program.\
[Install Docker Engine](https://docs.docker.com/engine/install/)

## Usage

```bash
usage: main.py [-h] --board_length [BOARD_LENGTH] --num_colors [{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26}] --player_name [{EndGame_b1,EndGame_b2}] --scsa_name
               [{InsertColors,TwoColor,ABColor,TwoColorAlternating,OnlyOnce,FirstLast,UsuallyFewer,PreferFewer}] --num_rounds [NUM_ROUNDS]
```

```bash
python3 main.py --board_length 4 --num_colors 6 --player_name EndGame_b2 --scsa_name TwoColorAlternating --num_rounds 10
```

## Docker

Build an image.
```bash
docker build . -t pydev
```

Run the image.
```bash
docker run -it --rm pydev --board_length 4 --num_colors 6 --player_name EndGame_b2 --scsa_name TwoColorAlternating --num_rounds 1
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

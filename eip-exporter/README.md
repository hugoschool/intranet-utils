# eip-exporter

Easily export all EIP projects

## Usage

```sh
uv run main.py --help
```

Exporting all EIP from all cities for 2028 promotion:
```sh
uv run main.py -y 2028
```

Exporting to an output file:
```sh
uv run main.py -y 2028 -o output.json
```

Exporting only `FR/LYN` for 2028 promotion:
```sh
uv run main.py -c FR/LYN -y 2028
```

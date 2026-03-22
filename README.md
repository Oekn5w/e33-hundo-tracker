## Livetracker for Expedition 33 100% Speedruns

Utility for displaying progression data during 100% Speedruns of Clair Obscur Expedition 33. As there is no in-game checklist and no definition of 100% this is based on what we can check for from reading the generated save files.

Pre-Order Bonuses are excluded from tracking, DLC items from the Thank You Update can be enabled.

Only NG items are tracked and also only items obtainable for Gustave in the Act I.

Tracked progression (base / DLC):
* Journals (49)
* Music Records (33)
* Pictos (193 / 210)
* Monoco's feet collection (46)
* Cosmetics (130 / 179)
* Weapons (103 / 116)

Cosmetics and Weapon progression is also available per character.

Note that some items are dependend on choices (Game ending and Clea's outfit from Flying Manor), for those only a single item each is counted against the total.

### Usage

The utility does not have a UI.

Launch it from commandline line via Python (probably most Python 3 versions work). `-h` gives the argument help.

The only required argument is the path to the Expedition savefile. There is no automatic searching for savefile location. You should select the file that will be there and updated during the run, for Steam these are found under `%LOCALAPPDATA%\Sandfall\Saved\SaveGames\<steam-id>\EXPEDITION-<num>.sav`.

The output path can be defined via `--out`, by default the `out` subfolder relative to the script is used. The output folder must exist!

To have the utility monitor the file for changes (aka progression), supply the `--monitor` argument. Exit the program via Crtl+C in that case. If the argument is not given the progression file are generated once and then returned to the command line.

Use argument `--dlc` to include items from the Thank You Update.

Output:
* `data.json`
* `obs_....txt`, if the `--obs` argument is supplied, can be used for GDI+ sources.
* `missing.json`, if the argument `--cheater` is supplied, contain the internal names of the missing items
* If the `--livesplit` argument is supplied, the data is attempted to be transmitted to a localhost Livesplit Webssocket server as Custom Variables (when implemented)

### Acknowledgements
The data for this utility is largely based on:
* [CO-E33_Save_editor](https://github.com/Infarctus/CO-E33_Save_editor)
* [Doc's 100% checklist](https://docs.google.com/spreadsheets/d/1lwLyNLFJ5SUqptNlauSuiFHRmkfFPn46VwlBL_pQwKE)

Conversion of the Unreal Engine Savefile via [uesave](https://github.com/trumank/uesave). A binary is included in this repository.

### License

See [License.md](./LICENSE.md)

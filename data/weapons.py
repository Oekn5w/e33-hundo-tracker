import copy

DATA_WEAPONS = {
    "V": {
        "Abysseram", # Abysseram
        "Blodam", # Blodam
        "Chaliso", # Dualiso
        "Chevalam", # Chevalam
        "Confuso", # Confuso
        "Corpeso", # Corpeso
        "Cruleram", # Cruleram
        "Cultam", # Cultam
        "Danseso", # Danseso
        "Delaram", # Delaram
        "Demonam", # Demonam
        "Gaulteram", # Gaulteram
        "Gesam", # Gesam
        "Glaceso", # Glaceso
        "Lanceram", # Lanceram
        "Moissoso", # Contorso
        "Noahram", # Noahram
        "Nosaram", # Nosaram
        "Reacheso_1", # Tireso
        "Reacheso_2", # Liteso
        "Sakaram", # Sakaram
        "Seeram", # Seeram
        "Simoso", # Simoso
        "Sireso_1", # Sireso
        "Sireso_2", # Dreameso
        "Verleso" # Verleso
    },
    "L": {
        "Angerim", # Angerim
        "Benisim", # Benisim
        "Betelim", # Betelim
        "Braselim", # Braselim
        "Chapelim", # Chapelim
        "Coralim", # Coralim
        "Deminerim", # Deminerim
        "Dualim", # Troubadim
        "Elerim", # Elerim
        "Lighterim", # Lighterim
        "Lunerim", # Lunerim
        "Painerim", # Painerim
        "Potierim", # Potierim
        "Reacherim_1", # Kralim
        "Reacherim_2", # Lithelim
        "Redalim", # Redalim
        "Saperim", # Saperim
        "Scaverim", # Scaverim
        "Sirenim_1", # Choralim
        "Sirenim_2", # Colim
        "Snowim", # Snowim
        "Trebuchim", # Trebuchim
    },
    "A": {
        "Battlum", # Battlum
        "Brulerum", # Brulerum
        "Chainebum", # Barrier Breaker
        "Clierum", # Clierum
        "Coldum", # Coldum
        "Duenum", # Duenum
        "Facesum", # Facesum
        "Glaisum", # Glaisum
        "Jarum", # Jarum
        "Maellum", # Maellum
        "Medalum", # Medalum
        "Melarum", # Melarum
        "Reachum_1", # Lithum
        "Reachum_2", # Plenum
        "Seashelum", # Seashelum
        "Sekarum", # Sekarum
        "Sirenum_1", # Tissenum
        "Sirenum_2", # Chantenum
        "Stalum", # Stalum
        "Troubadum", # Chalium
        "Veremum", # Veremum
        "Volesterum", # Volesterum
        "Yeverum" # Yeverum
    },
    "M": {
        "Boucharo", # Boucharo
        "Brumaro", # Brumaro
        "Chromaro", # Chromaro
        "Grandaro", # Grandaro
        "Joyaro", # Joyaro
        "Monocaro", # Monocaro
        "Reacharo_1", # Nusaro
        "Reacharo_2", # Fragaro
        "Sidaro", # Sidaro
        "Sirenaro_1", # Ballaro
        "Sirenaro_2", # Urnaro
    },
    "S": {
        "Algueron", # Algueron
        "Blizzon", # Blizzon
        "Bourgelon", # Bourgelon
        "Charnon", # Charnon
        "Chation", # Chation
        "Contorson", # Moisson
        "Corderon", # Corderon
        "Direton", # Direton
        "Garganon", # Garganon
        "Gobluson", # Gobluson
        "Hevason", # Hevason
        "Lusteson", # Lusteson
        "Minason", # Minason
        "Ramasson", # Ramasson
        "Rangeson", # Rangeson
        "Reacheron_1", # Guleson
        "Reacheron_2", # Litheson
        "Sadon", # Sadon
        "Scieleson", # Scieleson
        "Sirenon_1", # Tisseron
        "Sirenon_2", # Martenon
    }
}

DATA_WEAPONS_DLC = copy.deepcopy(DATA_WEAPONS)
DATA_WEAPONS_DLC["V"] |= {
    "VD_Verso_1", # Sucreso
    "VD_Verso_3", # Esquiso
}
DATA_WEAPONS_DLC["L"] |= {
    "Simonim", # Cleim
    "VD_Lune_1", # Bonbim
    "VD_Lune_2" # Esquim
}
DATA_WEAPONS_DLC["A"] |= {
    "VD_Maelle_1", # Licorum
    "VD_Maelle_2", # Esqium
}
DATA_WEAPONS_DLC["M"] |= {
    "Baguettaro", # Baguettaro
    "VD_Monoco_1", # Cannaro
    "VD_Monoco_2" # Esquiaro
}
DATA_WEAPONS_DLC["S"] |= {
    "Duollison", # Duollison
    "VD_Sciel_1", # Sucetton
    "VD_Sciel_2" # Esquion
}

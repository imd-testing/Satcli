import os
import steampowered

os.environ['STEAMPOWERED__DATABASE__SQL_ALCHEMY_CONN'] = f"postgresql+psycopg2://steampowered:ahshe0ookeS5upo9quohyuo8usoogu9ooph5arietoof1zu0be@localhost/steampowered"

steampowered.run_queue()

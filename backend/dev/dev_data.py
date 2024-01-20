from uuid import uuid4

import numpy

from backend.model import User, Item, Vote, BOOK, MODEL

user_ids = {
    "Richard Feynman": uuid4(),
    "Gary Gygax": uuid4(),
    "Mark Twain": uuid4(),
    "Bertrand Russell": uuid4(),
}

item_ids = {
    "Lectures in Physics": uuid4(),
    "Advanced Dungeons and Dragons": uuid4(),
    "Gamma Convergence for Beginners": uuid4(),
    "Connecticut Yankee": uuid4(),
    "Blades in the Dark": uuid4(),
    "Broken Compass": uuid4(),
    "Colostle: A Solo RPG Adventure": uuid4(),
    "Lore of Aetherra: The Lost Druid": uuid4(),
    "Thirsty Sword Lesbians": uuid4(),
    "Uncaged: Goddesses": uuid4(),
    "Wanderhome": uuid4(),
    "Root: The RPG": uuid4(),
    "Heart: The City Beneath": uuid4(),
    "Neverland: A Fantasy RPG System": uuid4(),
    "Vaesen - Nordic Horror Roleplaying": uuid4(),
    "Planet Apocalypse for 5th edition DnD": uuid4(),
}

item_imgs = {
    "Lectures in Physics": "https://m.media-amazon.com/images/I/81m7QsFdp5L._AC_UF1000,1000_QL80_.jpg",
    "Advanced Dungeons and Dragons": "https://m.media-amazon.com/images/I/A1iyMzLoadL._AC_UF1000,1000_QL80_.jpg",
    "Gamma Convergence for Beginners": "https://m.media-amazon.com/images/I/51fJxkKmlHL._AC_UF1000,1000_QL80_.jpg",
    "Connecticut Yankee": "https://m.media-amazon.com/images/I/51FfDxASpWL.jpg",
    "Blades in the Dark": "https://m.media-amazon.com/images/I/41rWfv49DxL._AC_.jpg",
    "Broken Compass": "https://m.media-amazon.com/images/I/71k4+ckJJlL._AC_UF894,1000_QL80_.jpg",
    "Colostle: A Solo RPG Adventure": "https://m.media-amazon.com/images/I/51s3rQUQORS._AC_UF1000,1000_QL80_.jpg",
    "Lore of Aetherra: The Lost Druid": "https://cf.geekdo-images.com/fB6W3jJKFTiBaDqPxN-pGA__imagepage/img/wHcvs88HEO8gwlQjKSLzimRvPQM=/fit-in/900x600/filters:no_upscale():strip_icc()/pic6586987.jpg",
    "Thirsty Sword Lesbians": "https://cf.geekdo-images.com/afuJxFS0RMqv1C7ybcmp0g__imagepage/img/Rx_ELEaKLFzdreNZPW6EJeDyUgk=/fit-in/900x600/filters:no_upscale():strip_icc()/pic6766526.jpg",
    "Uncaged: Goddesses": "https://cf.geekdo-images.com/ZnMPXkXpSrH6j4fcIO--fQ__imagepage/img/LE7-bZLi85HcnUogSou0hl-C6ME=/fit-in/900x600/filters:no_upscale():strip_icc()/pic6787091.jpg",
    "Wanderhome": "https://d1rbbjrn2xovty.cloudfront.net/000126/30/89/19/030891955858.jpg",
    "Root: The RPG": "https://d1vzi28wh99zvq.cloudfront.net/images/4353/373406.jpg",
    "Heart: The City Beneath": "https://ksr-ugc.imgix.net/assets/028/575/382/4504771e05f027617302307084f29117_original.jpg?ixlib=rb-2.1.0&auto=compress%2Cformat&q=1&w=700&fit=max&v=1585584352&frame=1&s=77d6e091b6a6a404c3ba0a1f5790cad2",
    "Neverland: A Fantasy RPG System": "https://images-us.bookshop.org/ingram/9781524860202.jpg?height=500&v=v2",
    "Vaesen - Nordic Horror Roleplaying": "https://www.modiphius.net/cdn/shop/products/vaesen-nordic-horror-roleplaying-core-book-vaesen-free-league-publishing-772053.jpg?v=1596627399",
    "Planet Apocalypse for 5th edition DnD": "https://d1vzi28wh99zvq.cloudfront.net/images/13031/380038.jpg",
}


users = [
    User(
        id=user_ids["Richard Feynman"],
        name="Richard Feynman",
        email="feynman@lanl.gov",
    ),
    User(
        id=user_ids["Gary Gygax"],
        name="Gary Gygax",
        email="gygax@tsr.com",
    ),
    User(
        id=user_ids["Mark Twain"],
        name="Mark Twain",
        email="twain@steam.com",
    ),
    User(
        id=user_ids["Bertrand Russell"],
        name="Bertrand Russell",
        email="russell@trin.cam.ac.uk",
    ),
]

item_types = [BOOK, MODEL]

items = [
    Item(
        id=item_ids[i],
        type_=item_types[n % len(item_types)],
        owner_id=users[n % len(users)].id,
        title=i,
        img_location=item_imgs[i],
        is_available=numpy.random.choice([True, False], p=[0.8, 0.2]),
        is_hidden=numpy.random.choice([True, False], p=[0.2, 0.8]),
    )
    for n, i in enumerate(item_ids)
]


votes = [
    Vote(
        item_id=item_ids["Lectures in Physics"],
        user_id=user_ids["Richard Feynman"],
    ),
    Vote(
        item_id=item_ids["Lectures in Physics"],
        user_id=user_ids["Gary Gygax"],
    ),
    Vote(
        item_id=item_ids["Advanced Dungeons and Dragons"],
        user_id=user_ids["Richard Feynman"],
    ),
    Vote(
        item_id=item_ids["Gamma Convergence for Beginners"],
        user_id=user_ids["Richard Feynman"],
    ),
    Vote(
        item_id=item_ids["Gamma Convergence for Beginners"],
        user_id=user_ids["Mark Twain"],
    ),
]

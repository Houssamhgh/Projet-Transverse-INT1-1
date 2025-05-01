from Classes import Rope, Platform, SlopedPlatform


def generate_rope_chain():
    return [
        Rope(600, 50),
        Rope(1000, 150),
        Rope(1300, 200),
        Rope(2000, 100),
        Rope(2700, 70),
        Rope(3200, 100),
        Rope(3700, 80),
        Rope(4000, 50),
        Rope(5000, 100),
        ]

ropes = generate_rope_chain()


def generate_platforms():
    return [
        Platform(615, 400, 150, 10,bouncy=True),
        Platform(1050, 400, 150, 20,bouncy=False),
        Platform(1800, 400, 150, 20,bouncy=True),
        Platform(2700, 400, 150, 20,bouncy=False),
        Platform(3600, 400, 150, 20,bouncy=True),

    ]

platforms = generate_platforms()


def generate_slopes():
    return[
        SlopedPlatform(350, 300, 600, 400),
        SlopedPlatform(350, 100, 350,300 ),
        SlopedPlatform(4000,400, 4000, 300 ),
    ]

slopes=generate_slopes()
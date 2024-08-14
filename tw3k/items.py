# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class CharItem(Item):
    # define the fields for your item here like:
    GameItemID = Field()
    FullName = Field()
    FamilyName = Field()
    GivenName = Field()
    CourtesyName = Field()
    BirthYear = Field()
    Gender = Field()
    ArtSet = Field()
    Type = Field()
    FaceSet = Field()


class FacItem(Item):
    GameItemID = Field()
    FactionName = Field()
    FactionLeader = Field()
    Campaign = Field()
    Culture = Field()
    SubCulture = Field()
    MilitaryGroup = Field()
    FactionGroup = Field()
    Playable = Field()
    PoliticalParty = Field()
    Year = Field()
    Description = Field()


class BuildingItem(Item):
    GameItemID = Field()
    Name = Field()
    Level = Field()
    ChainName = Field()
    GroupName = Field()
    CreateTime = Field()
    CreateCost = Field()
    UpkeepCost = Field()
    FoodCost = Field()

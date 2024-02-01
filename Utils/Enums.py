from enum import Enum
from typing import List

from discord import SelectOption, PartialEmoji

from Assets import BotEmojis
################################################################################

__all__ = (
    "JobPosition",
    "TrainingLevel",
    "RequirementLevel",
    "Weekday",
    "Hours",
    "Timezone",
    "CompensationType",
    "Month",
    "Minutes",
    "Days",
    "ViewType",
)

################################################################################
class FroggeEnum(Enum):
    
    @property
    def proper_name(self) -> str:
        
        return self.name
    
################################################################################    
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        raise NotImplementedError
        
################################################################################
    @property
    def select_option(self) -> SelectOption:

        return SelectOption(label=self.proper_name, value=str(self.value))

################################################################################
class JobPosition(FroggeEnum):

    Null = 0
    AssistantManager = 1
    Bartender = 2
    Bard = 3
    Court = 4
    DancerSFW = 5
    DancerNSFW = 6
    DJ = 7
    Gamba = 8
    GambaFlex = 9
    Greeter = 10
    Host = 11
    Manager = 12
    MiscRPFlex = 13
    Pillow = 14
    Photographer = 15
    Security = 16
    ShoutRunner = 17
    ShowRunner = 18
    TarotReader = 19
    
################################################################################
    @property
    def proper_name(self) -> str:
        
        if self.value == 1:
            return "Assistant Manager"
        elif self.value == 5:
            return "Dancer (SFW)"
        elif self.value == 6:
            return "Dancer (NSFW)"
        elif self.value == 9:
            return "Gamba (Flex)"
        elif self.value == 13:
            return "Misc. RP (Flex)"
        elif self.value == 17:
            return "Shout Runner"
        elif self.value == 18:
            return "Show Runner"
        elif self.value == 19:
            return "Tarot Reader"
        else:
            return self.name
            
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [p.select_option for p in JobPosition if p.value != 0]
    
################################################################################
class TrainingLevel(FroggeEnum):
    
    Null = 0
    Active = 1
    OnHold = 2
    Inactive = 3
    Pending = 4
    
################################################################################
    @property
    def proper_name(self) -> str:
               
        return "On Hold" if self.value == 2 else self.name
    
################################################################################    
    @property
    def emoji(self) -> PartialEmoji:
        
        if self.value == 1:
            return BotEmojis.Check
        elif self.value == 2:
            return BotEmojis.Pause
        elif self.value == 3:
            return BotEmojis.Sleep
        elif self.value == 4:
            return BotEmojis.Construction
        else:
            return BotEmojis.Cross
        
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [p.select_option for p in TrainingLevel if p.value != 0]

################################################################################
class RequirementLevel(FroggeEnum):
    
    Null = 0
    Complete = 1
    InProgress = 2
    Incomplete = 3
    Waived = 4
    
################################################################################
    @property
    def proper_name(self) -> str:
        
        if self.value == 2:
            return "In Progress"
        
        return self.name
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [p.select_option for p in RequirementLevel if p.value != 0]

################################################################################    
    @property
    def emoji(self) -> PartialEmoji:

        if self.value == 1:
            return BotEmojis.Check
        elif self.value == 2:
            return BotEmojis.Stopwatch
        elif self.value == 4:
            return BotEmojis.Goose
        else:
            return BotEmojis.Cross
        
################################################################################
class Weekday(FroggeEnum):
    
    Null = 0
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [p.select_option for p in Weekday if p.value != 0]
    
################################################################################
class Hours(FroggeEnum):

    Unavailable = 0
    TwelveAM = 1
    OneAM = 2
    TwoAM = 3
    ThreeAM = 4
    FourAM = 5
    FiveAM = 6
    SixAM = 7
    SevenAM = 8
    EightAM = 9
    NineAM = 10
    TenAM = 11
    ElevenAM = 12
    TwelvePM = 13
    OnePM = 14
    TwoPM = 15
    ThreePM = 16
    FourPM = 17
    FivePM = 18
    SixPM = 19
    SevenPM = 20
    EightPM = 21
    NinePM = 22
    TenPM = 23
    ElevenPM = 24
    
################################################################################
    @property
    def proper_name(self) -> str:
        # Still missing 12:00 AM at the start. Will need to correct for that.
        
        # if self.value == 0:
        #     return "Unavailable"
        # 
        # # Correcting the mapping for 12:00 PM
        # if self.value == 24:
        #     return "12:00 AM"
        # 
        # # Correct mapping for AM and PM times
        # hour = self.value if self.value <= 12 else self.value - 12
        # period = "AM" if self.value < 12 else "PM"
        # 
        # # Special handling for 12 AM
        # if self.value == 12:
        #     period = "PM"
        # elif self.value == 24:
        #     hour = 12  # Handling for 12 PM at the end of the cycle
        # 
        # return f"{hour}:00 {period}"

        if self.value == 1:
            return "12:00 AM"
        elif self.value == 2:
            return "1:00 AM"
        elif self.value == 3:
            return "2:00 AM"
        elif self.value == 4:
            return "3:00 AM"
        elif self.value == 5:
            return "4:00 AM"
        elif self.value == 6:
            return "5:00 AM"
        elif self.value == 7:
            return "6:00 AM"
        elif self.value == 8:
            return "7:00 AM"
        elif self.value == 9:
            return "8:00 AM"
        elif self.value == 10:
            return "9:00 AM"
        elif self.value == 11:
            return "10:00 AM"
        elif self.value == 12:
            return "11:00 AM"
        elif self.value == 13:
            return "12:00 PM"
        elif self.value == 14:
            return "1:00 PM"
        elif self.value == 15:
            return "2:00 PM"
        elif self.value == 16:
            return "3:00 PM"
        elif self.value == 17:
            return "4:00 PM"
        elif self.value == 18:
            return "5:00 PM"
        elif self.value == 19:
            return "6:00 PM"
        elif self.value == 20:
            return "7:00 PM"
        elif self.value == 21:
            return "8:00 PM"
        elif self.value == 22:
            return "9:00 PM"
        elif self.value == 23:
            return "10:00 PM"
        elif self.value == 24:
            return "11:00 PM"
        else:
            return self.name

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [p.select_option for p in Hours]
    
################################################################################
    @staticmethod
    def adjusted_select_options(start: int) -> List[SelectOption]:
        
        ret = [o for o in Hours.select_options() if int(o.value) > start]
        ret.append(Hours(1).select_option)
        
        return ret
    
################################################################################
    @staticmethod
    def limited_select_options() -> List[SelectOption]:
        
        return [o for o in Hours.select_options() if o.value != "0"]
    
################################################################################
    @property
    def timestamp(self) -> str:
        
        START_TS = -22089600  # (4/20/1969 12:00 AM)
        STRIDE = 3600
        
        ts = START_TS + (self.value - 1) * STRIDE
    
        return f"<t:{ts}:t>"
    
################################################################################
class Timezone(FroggeEnum):
    
    Null = 0
    MIT = 1
    HST = 2
    AST = 3
    PST = 4
    MST = 5
    CST = 6
    EST = 7
    PRT = 8
    AGT = 9
    CAT = 10
    GMT = 11
    ECT = 12
    EET = 13
    EAT = 14
    NET = 15
    PLT = 16
    BST = 17
    VST = 18
    CTT = 19
    JST = 20
    AET = 21
    SST = 22
    NST = 23
    
################################################################################
    @property
    def proper_name(self) -> str:
        
        if self.value == 1:
            return "Midway Island Time"
        elif self.value == 2:
            return "Hawaii Standard Time"
        elif self.value == 3:
            return "Alaska Standard Time"
        elif self.value == 4:
            return "Pacific Standard Time"
        elif self.value == 5:
            return "Mountain Standard Time"
        elif self.value == 6:
            return "Central Standard Time"
        elif self.value == 7:
            return "Eastern Standard Time"
        elif self.value == 8:
            return "Puerto Rico and US Virgin Islands Time"
        elif self.value == 9:
            return "Argentina Standard Time"
        elif self.value == 10:
            return "Central African Time"
        elif self.value == 11:
            return "UTC/Greenwich Mean Time"
        elif self.value == 12:
            return "European Central Time"
        elif self.value == 13:
            return "Eastern European Time"
        elif self.value == 14:
            return "Eastern African Time"
        elif self.value == 15:
            return "Near East Time"
        elif self.value == 16:
            return "Pakistan Lahore Time"
        elif self.value == 17:
            return "Bangladesh Standard Time"
        elif self.value == 18:
            return "Vietnam Standard Time"
        elif self.value == 19:
            return "China Taiwan Time"
        elif self.value == 20:
            return "Japan Standard Time"
        elif self.value == 21:
            return "Australia Eastern Time"
        elif self.value == 22:
            return "Solomon Standard Time"
        elif self.value == 23:
            return "New Zealand Standard Time"
        else:
            return self.name
    
################################################################################
    @property
    def description(self) -> str:
    
        if 1 <= self.value <= 23:
            offset = self.value - 12
            return f"(UTC{'+' if offset >= 0 else ''}{offset}:00)"
        else:
            return self.name
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [p.select_option for p in Timezone if p.value != 0]
    
################################################################################
    @property
    def select_option(self) -> SelectOption:
        
        return SelectOption(
            label=self.proper_name, description=self.description, value=str(self.value)
        )

################################################################################
    @property
    def utc_offset(self) -> int:

        return self.value - 12

################################################################################
class CompensationType(FroggeEnum):
    
    Null = 0
    Hourly = 1
    Flat = 2
    Commission = 3
    Other = 4
    
################################################################################
class Month(FroggeEnum):
    
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [p.select_option for p in Month]    
    
################################################################################
    def day_options(self) -> List[SelectOption]:
        
        ret = []
        
        for day in Days:
            if 0 < day.value <= 29:
                ret.append(day.select_option)
                
        if self.value != 2:
            ret.append(Days(30).select_option)
                
        if self.value in (1, 3, 5, 7, 8, 10, 12):
            ret.append(Days(31).select_option)
            
        return ret
    
################################################################################
class Minutes(FroggeEnum):
    
    Unavailable = 0
    Zero = 1
    Fifteen = 2
    Thirty = 3
    FortyFive = 4
    
################################################################################
    @property
    def proper_name(self) -> str:
        
        if self.value == 1:
            return ":00"
        elif self.value == 2:
            return ":15"
        elif self.value == 3:
            return ":30"
        elif self.value == 4:
            return ":45"
        else:
            return self.name

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [p.select_option for p in Minutes if p.value != 0]
    
################################################################################
    @staticmethod
    def hour_specific_select_options(hour: int) -> List[SelectOption]:
        
        if hour == 0:
            return [Minutes.Unavailable.select_option]
        
        hour -= 1
        if hour == 0:
            hour = 12
        elif hour > 12:
            hour -= 12
        
        return [
            SelectOption(
                label=f"{hour}{m.proper_name}",
                value=m.proper_name[1:]
            )
            for m in Minutes if m.value != 0
        ]

################################################################################
class Days(FroggeEnum):
        
    Unavailable = 0
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Eleven = 11
    Twelve = 12
    Thirteen = 13
    Fourteen = 14
    Fifteen = 15
    Sixteen = 16
    Seventeen = 17
    Eighteen = 18
    Nineteen = 19
    Twenty = 20
    TwentyOne = 21
    TwentyTwo = 22
    TwentyThree = 23
    TwentyFour = 24
    TwentyFive = 25
    TwentySix = 26
    TwentySeven = 27
    TwentyEight = 28
    TwentyNine = 29
    Thirty = 30
    ThirtyOne = 31
        
################################################################################
    @property
    def proper_name(self) -> str:
        
        if self.value in (1, 21, 31):
            suffix = "st"
        elif self.value in (2, 22):
            suffix = "nd"
        elif self.value in (3, 23):
            suffix = "rd"
        else:
            suffix = "th"
            
        return f"{self.value}{suffix}"
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [p.select_option for p in Days if p.value != 0]
    
################################################################################
class ViewType(Enum):
    
    StartTimeSelect = 1
    EndTimeSelect = 2
    
################################################################################
    
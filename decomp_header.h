typedef signed char int8_t;
typedef short int16_t;
typedef int int32_t;
typedef unsigned char uint8_t;
typedef unsigned short uint16_t;
typedef unsigned int uint32_t;
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef int8_t s8;
typedef int16_t s16;
typedef int32_t s32;
typedef u8 bool8;
typedef u16 bool16;
typedef u32 bool32;
#define TRUE 1
#define FALSE 0
#define NULL ((void *)0)

#define MAX_MON_MOVES 4
#define MAX_TEAM_MEMBERS 4
#define MAX_ROOM_COUNT 24
#define DUNGEON_MAX_SIZE_X 56
#define DUNGEON_MAX_SIZE_Y 32
#define DUNGEON_MAX_WILD_POKEMON 16
#define DUNGEON_MAX_POKEMON MAX_TEAM_MEMBERS + DUNGEON_MAX_WILD_POKEMON
#define NUM_MONSTERS 413
#define NUM_SPEED_COUNTERS 5
#define NUM_PREV_POS 4

struct Item
{
    u8 flags;
    u8 quantity;
    u8 id;
};

struct Move
{
    u8 moveFlags;
    u8 moveFlags2;
    u16 id;
    u8 PP;
    u8 ginseng; // How much the move is boosted by Ginsengs.
};

struct Position
{
    s16 x;
    s16 y;
};

struct Position32
{
    s32 x;
    s32 y;
};

enum CrossableTerrain
{
    CROSSABLE_TERRAIN_REGULAR = 0,
    CROSSABLE_TERRAIN_LIQUID = 1,
    CROSSABLE_TERRAIN_CREVICE = 2,
    CROSSABLE_TERRAIN_WALL = 3,
    NUM_CROSSABLE_TERRAIN
};

struct Tile
{
    // Uses the TerrainType bit flags.
    /* 0x0 */ u16 terrainType;
    u8 fill2[0x4 - 0x2];
    u16 unk4;
    u16 unk6;
    u8 unk8;
    /* 0x9 */ u8 room;
    // Bitwise flags for whether Pokémon can move to an adjacent tile. Bits correspond to directions in direction.h.
    // Different sets of flags are used for Pokémon that can cross special terrain, corresponding to the CrossableTerrain enum.
    /* 0xA */ u8 walkableNeighborFlags[NUM_CROSSABLE_TERRAIN];
    u8 fillE[0x10 - 0xE];
    /* 0x10 */ struct Entity *monster; // Pokémon on the tile.
    /* 0x14 */ struct Entity *object; // Item or trap on the tile.
};

struct RoomData
{
    u8 fill0[0x2 - 0x0];
    // All coordinates are inclusive.
    // These are not aligned properly to use the Position struct.
    /* 0x2 */ s16 bottomRightCornerX;
    /* 0x4 */ s16 bottomRightCornerY;
    /* 0x6 */ s16 topLeftCornerX;
    /* 0x8 */ s16 topLeftCornerY;
    u8 fillA[0x1A - 0xA];
};

struct Dungeon_sub
{
    u8 unk0;
    u8 unk1;
    u8 unk2;
};

struct DungeonLocation {
    u8 id;
    u8 floor;
};

struct DungeonMusicPlayer
{
    u32 state;
    u32 fadeOutSpeed;
    u16 fadeInSpeed;
    u16 songIndex;
    u16 pastSongIndex;
    u16 queuedSongIndex;
};

struct unkDungeonGlobal_unk1CE98_sub
{
    /* 0x0 */ u8 buffer1[0xA];
    /* 0xA */ u8 buffer2[0xA];
    /* 0x14 */ s16 unk14;
    /* 0x16 */ u8 fill16[0x2];
    /* 0x18 */ struct DungeonLocation dungeonLocation;
    /* 0x1C */ struct Item heldItem;
    /* 0x20 */ u32 exp;
    /* 0x24 */ s16 maxHPStat;
    /* 0x26 */ u8 atk;
    /* 0x27 */ u8 spAtk;
    /* 0x28 */ u8 def;
    /* 0x29 */ u8 spDef;
    /* 0x2A */ u8 level;
    /* 0x2B */ u8 attBoost;
    /* 0x2C */ u8 spAttBoost;
    /* 0x2D */ u8 defBoost;
    /* 0x2E */ u8 spDefBoost;
    u8 unk4; // speedBoost?
};

extern struct Dungeon *gDungeon;

struct Dungeon
{
    u8 unk0;
    u8 unk1;
    u8 unk2;
    u8 unk3;
    u8 unk4;
    u8 fill5[0x7 - 0x5];
    u8 unk7;
    u8 unk8;
    u8 fill9[0xC - 0x9];
    u8 unkC;
    u8 unkD;
    u8 unkE;
    /* 0xF */ bool8 noActionInProgress; // Whether the game is currently accepting input. Set to false while action animations play.
    u8 unk10;
    u8 unk11;
    s16 unk12;
    u8 fill14[0xB8 - 0x14];
    struct Entity *unkB8;
    u32 unkBC;
    u8 fillC0[0x16D - 0xC0];
    u8 unk16D;
    u8 fill16E[0x179 - 0x16E];
    /* 0x179 */ bool8 pokemonExposed; // True if a Pokémon on the floor has the Exposed status.
    u8 fill17A[0x17C - 0x17A];
    struct Dungeon_sub unk17C[0x100];
    /* 0x57C */ u8 fill57C[0x644 - 0x57c];
    /* 0x644 */ struct DungeonLocation dungeonLocation;
    u8 fill646[0x654 - 0x648];
    u8 unk654;
    u8 fill655[0x65C - 0x655];
    u8 unk65C;
    u8 fill65D[0x660 - 0x65D];
    /* 0x660 */ s16 fractionalTurn; // Handles turn order when Pokémon have different movement speeds.
    u8 fill662[0x666 - 0x662];
    /* 0x666 */ u16 windTurns; // Turns remaining before getting swept out of the dungeon.
    u8 fill668[0x66A - 0x668];
    u16 unk66A;
    u8 unk66C;
    u8 unk66D;
    /* 0x66E */ u8 unk66E;
    u8 unk66F;
    u8 unk670;
    /* 0x671 */ bool8 monsterHouseTriggered;
    /* 0x672 */ u8 unk672;
    u8 unk673;
    u8 unk674;
    u8 unk675;
    /* 0x676 */ bool8 itemHoldersIdentified;
    u8 unk677;
    u8 unk678;
    u8 unk679[0x68A - 0x679];
    /* 0x68A */ u8 unk68A;
    u8 fill68B[0x699 - 0x68B];
    u8 unk699;   
    u8 fill69A[0x363C - 0x69A];
    /* 0x363C */ u8 expYieldRankings[NUM_MONSTERS];
    u8 fill37E3[0x37F4 - 0x37D9];
    /* 0x37F4 */ s32 unk37F4;
    /* 0x37F8 */ bool8 plusIsActive[2]; // Index 0: Enemy , Index 1: Team
    /* 0x37FA */ bool8 minusIsActive[2]; // Index 0: Enemy , Index 1: Team 
    /* 0x37FC */ bool8 decoyActive;
    u8 fill37FD[0x3A0D - 0x37FD];
    /* 0x3A0D */ u8 unk3A0D;
    /* 0x3A0E */ s16 tileset;
    /* 0x3A10 */ u16 unk3A10;
    u8 fill3A10[0x3A14 - 0x3A12];
    /* 0x3A14 */ s16 bossBattleIndex;
    /* 0x3A18 */ struct Tile tiles[DUNGEON_MAX_SIZE_Y][DUNGEON_MAX_SIZE_X];
    u8 fillE218[0xE23C - 0xE218];
    s16 unkE23C;
    s16 unkE23E;
    u8 fillE240[0xE264 - 0xE240];
    /* 0xE264 */ u8 weather; // Uses the weather constants in weather.h.
    u8 unkE265; // Uses the weather constants in weather.h
    /* 0xE266 */ u8 weatherDamageCounter; // Timer for applying sandstorm/hail damage periodically.
    u8 unkE267[0xE26B - 0xE267];
    u8 unkE26B;
    u8 weatherTurns;
    u8 fillE26D[0xE26F - 0xE26D];
    /* 0xE26F */ u8 naturalWeather[8]; // The weather at the start of the floor. If the weather changes, then expires, revert back to the starting weather.
    /* 0xE277 */ u8 mudSportTurns;
    /* 0xE278 */ u8 waterSportTurns;
    /* 0xE279 */ bool8 nullifyWeather; // Air Lock and Cloud Nine toggle this to disable weather effects
    u8 fillE27A[0xE8C0 - 0xE27A];
    /* 0xE8C0 */ struct Tile* tilePointers[DUNGEON_MAX_SIZE_Y][DUNGEON_MAX_SIZE_X];
    u8 fill104C0[0x104C4 - 0x104C0];
    /* 0x104C4 */ struct RoomData roomData[MAX_ROOM_COUNT];
    u8 fill10764[0x10844 - 0x10764];
    /* 0x10844 */ s16 naturalJunctionListCounts[MAX_ROOM_COUNT];
    u8 fill10874[0x10884 - 0x10874];
    /* 0x10884 */ struct Position naturalJunctionList[MAX_ROOM_COUNT][32]; // Arrays of room exits for each room.
    u8 fill11444[0x11884 - 0x11484];
    u8 unk11884[0x1194];
    u8 fill12A18[0x12C24 - 0x12A18];
    u8 unk12C24[0x930];
    u8 fill13554[0x1356C - 0x13554];
    u8 unk1356C;
    u8 fill1356D[0x13570 - 0x1356D];
    /* 0x13570 */ u8 unk13570;
    u8 fill13571[0x13574 - 0x13571];
    /* 0x13574 */ u16 unk13574;
    /* 0x13576 */ u16 unk13576;
    /* 0x13578 */ u8 unk13578;
    /* 0x13579 */ u8 unk13579;
    u8 fill1357A[0x1357C - 0x1357A];
    /* 0x1357C */ struct Entity *teamPokemon[MAX_TEAM_MEMBERS];
    /* 0x1358C */ struct Entity *wildPokemon[DUNGEON_MAX_WILD_POKEMON];
    /* 0x135CC */ struct Entity *allPokemon[DUNGEON_MAX_POKEMON]; // Contains both team and wild Pokémon
    /* 0x1361C */ struct Entity *clientPokemon[2]; // Not sure how large this array is.
    u8 fill13624[0x17B2C - 0x13624];
    /* 0x17B2C */ struct Entity *lightningRodPokemon;
    /* 0x17B30 */ struct Entity *snatchPokemon;
    /* 0x17B34 */ u8 fillunk1734[0x17B38 - 0x17B34];
    /* 0x17B38 */ u32 unk17B38;
    /* 0x17B3C */ u32 unk17B3C;
    u8 fill17B40[0x181E8 - 0x17B40];
    /* 0x181E8 */ struct Position cameraPos;
    /* 0x181EC */ struct Position cameraPosMirror;
    /* 0x181F0 */ struct Position cameraPixelPos;
    /* 0x181F4 */ struct Position cameraPixelPosMirror;
    /* 0x181F8 */ struct Entity *cameraTarget;
    u32 unk181FC;
    u32 unk18200;
    u32 unk18204;
    u8 unk18208;
    /* 0x18209 */ u8 visibilityRange; // Dungeon light level.
    /* 0x1820A */ bool8 blinded; // Blacks out the screen when the player has the Blinker status.
    u8 unk1820B;
    u32 unk1820C;
    /* 0x18210 */ bool8 hallucinating; // Displays Substitute and flower sprites when the player has the Cross-Eyed status.
    u8 fill18211[0x18217 - 0x18211];
    u8 unk18217;
    u8 fill18218[0x1C578 - 0x18218];
    u8 unk1C578;
    u8 fill1C579[0x1CE98 - 0x1C579];
    /* 0x1CE98 */ struct unkDungeonGlobal_unk1CE98_sub unk1CE98;
    u32 unk1CEC8;
    /* 0x1CECC */ struct DungeonMusicPlayer musPlayer;
};

struct ActionContainer
{
    /* 0x0 */ u16 action;
    /* 0x2 */ u8 direction;
    u8 fill3;
    // Additional parameter alongside actionIndex. Used for things like indicating which move a Pokémon should use from its moveset.
    /* 0x4 */ u8 actionUseIndex;
    // Position of the Pokémon the last time it threw an item.
    /* 0x8 */ struct Position lastItemThrowPosition;
    u8 unkC;
    u8 fillD[3];
    u8 fill10[4];
    // Position of the target that the Pokémon wants throw an item at.
    /* 0x14 */ struct Position itemTargetPosition;
};

// Used for Pokémon, items, and traps.
struct Entity
{
    /* 0x0 */ u32 type;
    /* 0x4 */ struct Position pos;
    /* 0x8 */ struct Position prevPos;
    // The center of the entity acccording to pixel-space coordinates, using the same origin as posWorld.
    // X = (posWorld * 24 + 16) * 256, while Y = (posWorld * 24 + 12) * 256.
    /* 0xC */ struct Position32 pixelPos;
    /* 0x14 */ struct Position32 prevPixelPos;
    s32 unk1C;
    /* 0x20 */ bool8 isVisible; // Turned off when a Pokémon faints.
    u8 fill21[0x25 - 0x21];
    /* 0x25 */ u8 room;
    // The global spawn index counter starts at 10. Each Pokémon that spawns increments the counter and
    // gets assigned the current counter value as its spawn index.
    /* 0x26 */ u16 spawnGenID;
    u8 fill28[0x2A - 0x28];
    // 0x2A and 0x2E seem to be related to the sprite animation, though not sure how they're related.
    /* 0x2A */ u16 spriteAnimationCounter;
    // Each animation has a few different sprites that it transitions between.
    // This is the index of the currently displayed sprite within the animation.
    // Differs from 0x34 as this index is only between the sprites used by the animation,
    // while 0x34 is a shared index among all sprites.
    /* 0x2C */ u16 spriteAnimationIndex;
    /* 0x2E */ u16 spriteAnimationCounter2;
    // The position of the sprite within the tile. The animation may change the position slightly.
    /* 0x30 */ struct Position spritePos;
    // Offset of the sprite from its position at the start of the animation. Changes alongside spritePos.
    /* 0x34 */ struct Position spritePosOffset;
    u8 fill38[0x48 - 0x38];
    // The sprite index to display, among the Pokémon's possible sprites.
    /* 0x48 */ u16 spriteIndexForEntity;
    /* 0x4A */ u16 spriteIndexForEntity2;
    u8 unk4C[0x50 - 0x4C];
    // Some kind of base sprite index depending on which way the Pokémon is facing.
    // and which animation is playing (e.g., idle, moving).
    // Compared to 0x48, 0x50 and 0x54 are much larger and could be global indexes among all sprites in the game.
    /* 0x50 */ u16 spriteBaseForDirection;
    u8 fill52[0x54 - 0x52];
    /* 0x54 */ u16 spriteGlobalIndex;
    u8 fill56[0x64 - 0x56];
    u32 unk64;
    u8 fill68[2];
    /* 0x6A */ u8 unk6A;
    /* 0x6A */ u8 unk6B;
    /* 0x6C */ u8 direction;
    /* 0x6D */ u8 direction2; // Duplicate of 0x6C?
    /* 0x70 */ struct EntityInfo *info;
};

struct EntityInfo
{
    // This has different purposes for Pokémon, items, and traps.
    // Pokemon: MovementFlag
    // Items: ItemFlag
    // Traps: TrapType
    /* 0x0 */ u16 flags;
    /* 0x2 */ s16 id; // Pokémon species or item ID.
    // Everything from here on only applies to Pokémon.
    /* 0x4 */ s16 apparentID; // Shows a different Pokémon when using Transform.
    /* 0x6 */ bool8 isNotTeamMember;
    /* 0x7 */ bool8 isTeamLeader;
    /* 0x8 */ u8 shopkeeper;
    /* 0x9 */ u8 level;
    /* 0xA */ u8 teamIndex; // Leader is 0, partner is 1, etc.
    /* 0xC */ s16 IQ;
    /* 0xE */ s16 HP;
    /* 0x10 */ s16 maxHPStat;
    // Bosses have higher HP than normal for their level. This is the max HP they would normally have given their level.
    /* 0x12 */ s16 originalHP;
    /* 0x14 */ u8 atk;
    /* 0x15 */ u8 spAtk;
    /* 0x16 */ u8 def;
    /* 0x17 */ u8 spDef;
    /* 0x18 */ u32 exp;
    // Temporary stat boosts/drops from effects like Growl or Swords Dance.
    // These start at 10 and are in the range [1, 19].
    // Index 0 is Attack. Index 1 is Special Attack.
    /* 0x1C */ s16 offensiveStages[2];
    // Index 0 is Defense. Index 1 is Special Defense.
    /* 0x20 */ s16 defensiveStages[2];
    // Index 0 is accuracy. Index 1 is evasion.
    /* 0x24 */ s16 hitChancesStages[2];
    // // When a Fire-type move is used on a Pokémon with Flash Fire, this value increases the power of the Pokémon's Fire-type moves.
    /* 0x28 */ s16 flashFireBoost;
    // These start at 0x1000, and are halved by certain moves like Screech to lower the corresponding stat.
    // Index 0 is Attack. Index 1 is Special Attack.
    /* 0x2C */ s32 offensiveMultipliers[2];
    // Index 0 is Defense. Index 1 is Special Defense.
    /* 0x34 */ s32 defensiveMultipliers[2];
    /* 0x3C */ s16 hiddenPowerBasePower;
    /* 0x3E */ u8 hiddenPowerType;
    u8 fill3F;
    /* 0x40 */ u8 joinedAt; // Uses the dungeon index in dungeon.h.
    /* 0x44 */ struct ActionContainer action;
    /* 0x5C */ u8 types[2];
    /* 0x5E */ u8 abilities[2];
    /* 0x60 */ struct Item heldItem;
    u8 fill64[0x68 - 0x64];
    /* 0x68 */ struct Position prevPos[NUM_PREV_POS];
    /* 0x78 */ u8 aiObjective;
    /* 0x79 */ bool8 aiNotNextToTarget;
    /* 0x7A */ bool8 aiTargetingEnemy;
    /* 0x7B */ bool8 aiTurningAround;
    /* 0x7C */ u16 aiTargetSpawnGenID;
    /* 0x80 */ struct Entity *aiTarget;
    u8 fill84[0x88 - 0x84];
    /* 0x88 */ struct Position aiTargetPos;
    // Bitwise flags corresponding to selected IQ skills.
    /* 0x8C */ u8 IQSkillMenuFlags[4]; // IQ skills selected in the IQ skills menu.
    /* 0x90 */ u8 IQSkillFlags[4];
    /* 0x94 */ u8 tactic;
    u8 fill95[0x98 - 0x95];
    /* 0x98 */ u32 unk98;
    /* 0x9C */ u32 unk9C;
    /* 0xA0 */ u32 unkA0;
    /* 0xA4 */ u8 clientType;
    u8 fillA5[0xA8 - 0xA5];
    // Statuses are split into groups based on which ones can't overlap.
    // See status.h for which statuses are in each group.
    /* 0xA8 */ u8 sleep;
    /* 0xA9 */ u8 sleepTurns;
    u8 fillAA[0xAC - 0xAA];
    /* 0xAC */ u8 nonVolatileStatus;
    /* 0xAD */ u8 nonVolatileStatusTurns;
    /* 0xAE */ u8 nonVolatileStatusDamageCountdown;
    u8 fillAF;
    /* 0xB0 */ u8 immobilizeStatus;
    u8 fillB1[0xB4 - 0xB1];
    /* 0xB4 */ s32 unkB4;
    /* 0xB8 */ u8 immobilizeStatusTurns;
    /* 0xB9 */ u8 immobilizeStatusDamageCountdown;
    u8 fillBA[0xBC - 0xBA];
    /* 0xBC */ u8 volatileStatus;
    /* 0xBD */ u8 volatileStatusTurns;
    u8 fillBE[0xC0 - 0xBE];
    /* 0xC0 */ u8 chargingStatus;
    /* 0xC1 */ u8 chargingStatusTurns;
    /* 0xC2 */ u8 chargingStatusMoveIndex; // The position of the move in the Pokémon's moveset that triggered the status.
    u8 fillC3;
    /* 0xC4 */ u8 protectionStatus;
    /* 0xC5 */ u8 protectionStatusTurns;
    u8 fillC6[0xC8 - 0xC6];
    /* 0xC8 */ u8 waitingStatus;
    /* 0xC9 */ bool8 enemyDecoy; // True if the Pokémon is a decoy and a wild Pokémon (i.e., not an allied Pokémon).
    u8 fillCA;
    /* 0xCB */ u8 waitingStatusTurns;
    /* 0xCC */ u8 curseDamageCountdown;
    u8 fillCD[0xD0 - 0xCD];
    /* 0xD0 */ u8 linkedStatus;
    u8 fillD1[0xD4 - 0xD1];
    /* 0xD4 */ u32 unkD4;
    /* 0xD8 */ u8 unkD8;
    /* 0xD9 */ u8 linkedStatusTurns;
    /* 0xDA */ u8 linkedStatusDamageCountdown;
    u8 fillDB;
    /* 0xDC */ u8 moveStatus;
    /* 0xDD */ u8 moveStatusTurns;
    u8 fillDE[0xE0 - 0xDE];
    /* 0xE0 */ u8 itemStatus;
    u8 fillE1[0xE4 - 0xE1];
    /* 0xE4 */ u8 transformStatus;
    /* 0xE5 */ u8 transformStatusTurns;
    u8 fillE6[0xE8 - 0xE6];
    /* 0xE8 */ u8 eyesightStatus;
    /* 0xE9 */ u8 eyesightStatusTurns;
    /* 0xEA */ u8 unkEA;
    u8 fillEB;
    /* 0xEC */ bool8 muzzled;
    /* 0xED */ u8 muzzledTurns;
    u8 fillEE[0xF0 - 0xEE];
    /* 0xF0 */ bool8 powerEars;
    /* 0xF1 */ bool8 scanning;
    /* 0xF2 */ bool8 stairSpotter;
    u8 fillF3;
    /* 0xF4 */ bool8 grudge;
    /* 0xF5 */ bool8 exposed;
    /* 0xF6 */ bool8 isColorChanged;
    /* 0xF7 */ bool8 bossFlag;
    /* 0xF8 */ bool8 speedStageChanged; // Toggled when pokemon is movement speed is sped up
    /* 0xF9 */ u8 unkF9;
    /* 0xFA */ u8 terrifiedTurns; // Doubles as a bool for whether the Pokémon is terrified.
    u8 unkFB;
    // Set to true if the player makes a teammate use their held item.
    // This is done by going to the teammate's held item in the toolbox and selecting "Use".
    /* 0xFC */ bool8 useHeldItem;
    /* 0xFD */ u8 perishSongTurns; // When this reaches 0, the Pokémon faints from Perish Song. Doubles as a bool for whether the Pokémon is afflicted by Perish Song.
    u8 unkFE;
    u8 unkFF;
    /* 0x100 */ u8 targetingDecoy; // If the Pokémon is targeting a decoy, this indicates whether the decoy target is a team or wild Pokémon.
    /* 0x104 */ s32 speedStage;
    // The turn counter for movement speed up/down is split into five timers each. Multiple timers are used if the Pokémon is affected by multiple
    // speed-up/slow effects at once, like using Agility twice.
    /* 0x108 */ u8 speedUpCounters[NUM_SPEED_COUNTERS];
    /* 0x10D */ u8 speedDownCounters[NUM_SPEED_COUNTERS];
    /* 0x112 */ u8 stockpileStage;
    u8 fill113;
    // When non-zero, an AI Pokémon will move in a random direction every turn.
    // Unclear where this is set in-game; it is not set by statuses (e.g., confusion) or mission clients.
    /* 0x114 */ u32 moveRandomly;
    /* 0x118 */ struct Move moves[MAX_MON_MOVES];
    /* 0x138 */ u8 struggleMoveFlags;
    /* 0x13C */ u32 belly;
    /* 0x140 */ u32 maxBelly;
    /* 0x144 */ bool8 aiNextToTarget; // True if an AI Pokémon is following another Pokémon and is already adjacent to them.
    /* 0x145 */ bool8 recalculateFollow; // Used by the AI to defer a movement decision until after all other Pokémon have moved.
    u8 fill146;
    /* 0x147 */ bool8 waiting; // True if an AI Pokémon decided to do nothing this turn.
    /* 0x148 */ bool8 attacking;
    /* 0x149 */ u8 unk149;
    /* 0x14A */ u8 unk14A;
    u8 fill14B[0x14E - 0x14B];
    /* 0x14E */ u16 visualFlags;
    /* 0x150 */ u16 previousVisualFlags;
    /* 0x152 */ u8 unk152;
    u8 unk153;
    u8 unk154;
    u8 unk155;
    u8 fill158[0x158 - 0x156];
    u8 unk158;
    u8 unk159;
    u8 unk15A;
    u8 unk15B;
    u8 unk15C;
    u8 unk15D;
    u8 unk15E;
    u8 unk15F;
    u8 fill160[0x164 - 0x160];
    /* 0x164 */ u8 unk164;
    /* 0x165 */ u8 unk165;
    u8 fill166[0x169 - 0x166];
    u8 turnsSinceWarpScarfActivation;
    /* 0x16C */ struct Position targetPos;
    /* 0x170 */ struct Position pixelPos;
    u32 unk174;
    u8 fill178[0x17A - 0x178];
    /* 0x17A */ u16 mimicMoveIDs[MAX_MON_MOVES]; // All moves that Mimic has copied (not sure on size...)
    // Previous value of targetPosition for movement, 1 and 2 moves ago.
    /* 0x184 */ struct Position previousTargetMovePosition1;
    /* 0x188 */ struct Position32 previousTargetMovePosition2;
    /* 0x190 */ u8 lastMoveDirection; // The last direction that the Pokémon moved in.
    // Number of tiles that the Pokémon moved last, multiplied by 0x100.
    /* 0x194 */ struct Position32 lastMoveIncrement;
    /* 0x19C */ u8 walkAnimFramesLeft; // Set when the Pokémon starts moving, and counts down until the Pokémon's walk animation stops.
    u8 fill19D[0x1F4 - 0x19D];
    /* 0x1F4 */ u8 numMoveTiles; // Number of tiles to move in a turn. Can be greater than 1 if the user's movement speed is boosted.
    u8 fill1F5;
    /* 0x1F6 */ bool8 notMoving;
    u8 fill1F7[0x1FA - 0x1F7];
    /* 0x1FA */ s16 mobileTurnTimer; // When a Pokémon can pass through walls in a hallway, this counts up to 200 before the Pokémon turns in a random direction.
    /* 0x1FC */ u16 expGainedInTurn; // Used to accumulate experience when multiple enemies are defeated in one turn.
    /* 0x200 */ u32 statusIcons;
    u8 unk204;
};

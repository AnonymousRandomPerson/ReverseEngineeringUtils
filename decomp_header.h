#include "global.h"

#define MAX_MON_MOVES 4
#define MAX_TEAM_MEMBERS 4
#define MAX_ROOM_COUNT 24
#define DUNGEON_MAX_SIZE_X 55
#define DUNGEON_MAX_SIZE_Y 31
#define DUNGEON_MAX_WILD_POKEMON 16
#define DUNGEON_MAX_POKEMON MAX_TEAM_MEMBERS + DUNGEON_MAX_WILD_POKEMON
#define NUM_SPECIES 413

struct ItemSlot
{
    u8 itemFlags;
    u8 numItems;
    u8 itemIndex;
};

struct PokemonMove
{
    u8 moveFlags;
    bool8 sealed;
    u16 moveID;
    u8 pp;
    u8 powerBoost; // How much the move is boosted by Ginsengs.
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

struct MapTile
{
    // Uses the TileType bit flags.
    /* 0x0 */ u16 tileType;
    u8 fill2[0x4 - 0x2];
    u16 unk4;
    u16 unk6;
    u8 unk8;
    /* 0x9 */ u8 roomIndex;
    // Bitwise flags for whether Pokémon can move to an adjacent tile. Bits correspond to directions in direction.h.
    // Different sets of flags are used for Pokémon that can cross special terrain.
    /* 0xA */ u8 canMoveAdjacent;
    /* 0xB */ u8 canMoveAdjacentLiquid;
    /* 0xC */ u8 canMoveAdjacentCrevice;
    /* 0xD */ u8 canMoveAdjacentWall;
    u8 fillE[0x10 - 0xE];
    /* 0x10 */ struct DungeonEntity *pokemon; // Pokémon on the tile.
    /* 0x14 */ struct DungeonEntity *mapObject; // Item or trap on the tile.
};

struct MapRoom
{
    u8 fill0[0x2 - 0x0];
    // All coordinates are inclusive.
    /* 0x2 */ struct Position start;
    /* 0x6 */ struct Position end;
    u8 fillA[0x1C - 0xA];
};

extern struct DungeonGlobalData *gDungeonGlobalData;

struct DungeonGlobalData
{
    u8 unk0;
    u8 unk1;
    u8 unk2;
    u8 unk3;
    u8 unk4;
    u8 fill5[0x7 - 0x5];
    u8 unk7;
    u8 fill8[0xF - 0x8];
    /* 0xF */ bool8 inputAllowed; // Whether the game is currently accepting input. Set to false while action animations play.
    u8 fill10;
    u8 unk11;
    u8 fill12[0x16D - 0x12];
    u8 unk16D;
    u8 fill16E[0x179 - 0x16E];
    /* 0x179 */ bool8 pokemonExposed; // True if a Pokémon on the floor has the Exposed status.
    u8 fill17A[0x645 - 0x17A];
    /* 0x645 */ u8 floorNumber;
    u8 fill646[0x65C - 0x646];
    u8 unk65C;
    u8 fill65D[0x660 - 0x65D];
    /* 0x660 */ u8 speedTurnCounter; // Handles turn order when Pokémon have different movement speeds.
    u8 fill661[0x666 - 0x661];
    /* 0x666 */ u16 turnsLeft; // Turns remaining before getting swept out of the dungeon.
    u8 fill668[0x66A - 0x668];
    u16 unk66A;
    u8 fill66C[0x671 - 0x66C];
    /* 0x671 */ bool8 monsterHouseActive;
    /* 0x672 */ u8 unk672;
    u8 fill673[0x363C - 0x673];
    /* 0x363C */ u8 expYieldRankings[NUM_SPECIES];
    u8 fill37E3[0x37FC - 0x37D9];
    /* 0x37FC */ bool8 decoyActive;
    u8 fill37FD[0x3A0D - 0x37FD];
    /* 0x3A0D */ u8 unk3A0D;
    /* 0x3A0E */ s16 tileset;
    u8 fill3A10[0x3A14 - 0x3A10];
    /* 0x3A14 */ s16 bossBattleIndex;
    u8 fill3A16[0x3A18 - 0x3A16];
    /* 0x3A18 */ struct MapTile mapTiles[DUNGEON_MAX_SIZE_X * DUNGEON_MAX_SIZE_Y];
    u8 fill54BC[0xE23C - 0xD9F0];
    s16 unkE23C;
    s16 unkE23E;
    u8 fillE240[0xE264 - 0xE240];
    /* 0xE264 */ u8 weather; // Uses the weather constants in weather.h.
    u8 unkE265;
    /* 0xE266 */ u8 weatherDamageTimer; // Timer for applying sandstorm/hail damage periodically.
    u8 fillE266[0xE26B - 0xE267];
    u8 unkE26B;
    u8 weatherTurnsLeft;
    u8 fillE26D[0xE270 - 0xE26D];
    /* 0xE270 */ u8 startingWeather; // The weather at the start of the floor. If the weather changes, then expires, revert back to the starting weather.
    u8 fillE271[0xE277 - 0xE271];
    /* 0xE277 */ u8 mudSportTurnsLeft;
    /* 0xE278 */ u8 waterSportTurnsLeft;
    u8 fillE279[0xE8C0 - 0xE279];
    /* 0xE8C0 */ u32 mapEntityPointers[DUNGEON_MAX_SIZE_X * DUNGEON_MAX_SIZE_Y];
    u8 fill10364[0x104C4 - 0x10364];
    /* 0x104C4 */ struct MapRoom roomData[MAX_ROOM_COUNT];
    u8 fill10604[0x10844 - 0x107C4];
    /* 0x10844 */ u16 numRoomExits[MAX_ROOM_COUNT];
    u8 fill10874[0x10884 - 0x10874];
    /* 0x10884 */ struct Position roomExits[MAX_ROOM_COUNT][32]; // Arrays of room exits for each room.
    u8 fill11444[0x1356C - 0x11484];
    u8 unk1356C;
    u8 fill1356D[0x1357C - 0x1356D];
    /* 0x1357C */ struct DungeonEntity *teamPokemon[MAX_TEAM_MEMBERS];
    /* 0x1358C */ struct DungeonEntity *wildPokemon[DUNGEON_MAX_WILD_POKEMON];
    /* 0x135CC */ struct DungeonEntity *allPokemon[DUNGEON_MAX_POKEMON]; // Contains both team and wild Pokémon
    /* 0x1361C */ struct DungeonEntity *clientPokemon[2]; // Not sure how large this array is.
    u8 fill13624[0x181F8 - 0x13624];
    /* 0x181F8 */ struct DungeonEntity *leader; // Pointer to the team leader.
    u32 unk181FC;
    u32 unk18200;
    u32 unk18204;
    u8 unk18208;
    /* 0x18209 */ u8 visibility; // Dungeon light level.
    /* 0x1820A */ bool8 displayBlinker; // Blacks out the screen when the player has the Blinker status.
    u8 unk1820B;
    u32 unk1820C;
    /* 0x18210 */ bool8 displayCrossEyed; // Displays Substitute and flower sprites when the player has the Cross-Eyed status.
    u8 fill18211[0x18217 - 0x18211];
    u8 unk18217;
};

struct DungeonActionContainer
{
    /* 0x0 */ u16 action;
    /* 0x2 */ s8 facingDir;
    u8 fill3;
    // Additional parameter alongside actionIndex. Used for things like indicating which move a Pokémon should use from its moveset.
    /* 0x4 */ u8 actionUseIndex;
    u8 fill5[0x8 - 0x5];
    // Position of the Pokémon the last time it threw an item.
    /* 0x8 */ struct Position lastItemThrowPosition;
    u8 unkC;
};

struct DungeonEntityData
{
    // This has different purposes for Pokémon, items, and traps.
    // Pokemon: MovementFlag
    // Items: ItemFlag
    // Traps: TrapType
    /* 0x0 */ u16 flags;
    /* 0x2 */ s16 entityID; // Pokémon species or item ID.
    // Everything from here on only applies to Pokémon.
    /* 0x4 */ s16 transformSpecies; // Shows a different Pokémon when using Transform.
    /* 0x6 */ bool8 isEnemy;
    /* 0x7 */ bool8 isLeader;
    /* 0x8 */ u8 shopkeeperMode;
    /* 0x9 */ u8 level;
    /* 0xA */ u8 partyIndex; // Leader is 0, partner is 1, etc.
    u8 fillB;
    /* 0xC */ u16 IQ;
    /* 0xE */ s16 HP;
    /* 0x10 */ s16 maxHP;
    // Bosses have higher HP than normal for their level. This is the max HP they would normally have given their level.
    /* 0x12 */ s16 originalHP;
    /* 0x14 */ u8 attack;
    /* 0x15 */ u8 specialAttack;
    /* 0x16 */ u8 defense;
    /* 0x17 */ u8 specialDefense;
    /* 0x18 */ u32 expPoints;
    // Temporary stat boosts/drops from effects like Growl or Swords Dance.
    // These start at 10 and are in the range [1, 19].
    /* 0x1C */ s16 attackStage;
    /* 0x1E */ s16 specialAttackStage;
    /* 0x20 */ s16 defenseStage;
    /* 0x22 */ s16 specialDefenseStage;
    /* 0x24 */ s16 accuracyStage;
    /* 0x26 */ s16 evasionStage;
    // // When a Fire-type move is used on a Pokémon with Flash Fire, this value increases the power of the Pokémon's Fire-type moves.
    /* 0x28 */ s16 flashFireBoost;
    u8 fill2A[0x2C - 0x2A];
    // These start at 0x1000, and are halved by certain moves like Screech to lower the corresponding stat.
    /* 0x2C */ s32 attackMultiplier;
    /* 0x30 */ s32 specialAttackMultiplier;
    /* 0x34 */ s32 defenseMultiplier;
    /* 0x38 */ s32 specialDefenseMultiplier;
    u8 fill3C[0x3E - 0x3C];
    /* 0x3E */ u8 hiddenPowerType;
    u8 fill3F;
    /* 0x40 */ u8 joinLocation; // Uses the dungeon index in dungeon.h.
    u8 fill41[0x44 - 0x41];
    /* 0x44 */ struct DungeonActionContainer action;
    u8 fill55[0x58 - 0x55];
    // Position of the target that the Pokémon wants throw an item at.
    /* 0x58 */ struct Position itemTargetPosition;
    /* 0x5C */ u8 type1;
    /* 0x5D */ u8 type2;
    /* 0x5E */ u8 ability1;
    /* 0x5F */ u8 ability2;
    /* 0x60 */ struct ItemSlot heldItem;
    u8 fill64[0x68 - 0x64];
    /* 0x68 */ struct Position previousPosition1;
    /* 0x6C */ struct Position previousPosition2;
    /* 0x70 */ struct Position previousPosition3;
    /* 0x74 */ struct Position previousPosition4;
    /* 0x78 */ u8 movementAction;
    /* 0x79 */ bool8 notAdjacentToTarget;
    /* 0x7A */ bool8 hasTarget;
    /* 0x7B */ bool8 turnAround;
    /* 0x7C */ u16 targetPokemonSpawnIndex;
    u8 fill7E[0x80 - 0x7E];
    /* 0x80 */ u32 targetPokemon;
    u8 fill84[0x88 - 0x84];
    /* 0x88 */ struct Position targetMovePosition;
    // Bitwise flags corresponding to selected IQ skills.
    /* 0x8C */ u8 IQSkillsSelected[4]; // IQ skills selected in the IQ skills menu.
    /* 0x90 */ u8 IQSkillsEnabled[4];
    /* 0x94 */ u8 tactic;
    u8 fill95[0xA4 - 0x95];
    /* 0xA4 */ u8 clientType;
    u8 fillA5[0xA8 - 0xA5];
    // Statuses are split into groups based on which ones can't overlap.
    // See status.h for which statuses are in each group.
    /* 0xA8 */ u8 sleepStatus;
    /* 0xA9 */ u8 sleepStatusTurnsLeft;
    u8 fillAA[0xAC - 0xAA];
    /* 0xAC */ u8 nonVolatileStatus;
    /* 0xAD */ u8 nonVolatileStatusTurnsLeft;
    /* 0xAE */ u8 nonVolatileStatusDamageTimer;
    u8 fillAF;
    /* 0xB0 */ u8 immobilizeStatus;
    u8 fillB1[0xB8 - 0xB1];
    /* 0xB8 */ u8 immobilizeStatusTurnsLeft;
    /* 0xB9 */ u8 immobilizeStatusDamageTimer;
    u8 fillBA[0xBC - 0xBA];
    /* 0xBC */ u8 volatileStatus;
    /* 0xBD */ u8 volatileStatusTurnsLeft;
    u8 fillBE[0xC0 - 0xBE];
    /* 0xC0 */ u8 chargingStatus;
    /* 0xC1 */ u8 chargingStatusTurnsLeft;
    /* 0xC2 */ u8 chargingStatusMoveIndex; // The position of the move in the Pokémon's moveset that triggered the status.
    u8 fillC3;
    /* 0xC4 */ u8 protectionStatus;
    /* 0xC5 */ u8 protectionStatusTurnsLeft;
    u8 fillC6[0xC8 - 0xC6];
    /* 0xC8 */ u8 waitingStatus;
    /* 0xC9 */ bool8 enemyDecoy; // True if the Pokémon is a decoy and a wild Pokémon (i.e., not an allied Pokémon).
    u8 fillCA;
    /* 0xCB */ u8 waitingStatusTurnsLeft;
    /* 0xCC */ u8 cursedDamageTimer;
    u8 fillCD[0xD0 - 0xCD];
    /* 0xD0 */ u8 linkedStatus;
    u8 fillD1[0xD9 - 0xD1];
    /* 0xD9 */ u8 linkedStatusTurnsLeft;
    /* 0xDA */ u8 linkedStatusDamageTimer;
    u8 fillDB;
    /* 0xDC */ u8 moveStatus;
    /* 0xDD */ u8 moveStatusTurnsLeft;
    u8 fillDE[0xE0 - 0xDE];
    /* 0xE0 */ u8 itemStatus;
    u8 fillE1[0xE4 - 0xE1];
    /* 0xE4 */ u8 transformStatus;
    /* 0xE5 */ u8 transformStatusTurnsLeft;
    u8 fillE6[0xE8 - 0xE6];
    /* 0xE8 */ u8 eyesightStatus;
    u8 fillE9;
    /* 0xEA */ u8 eyesightStatusTurnsLeft;
    u8 fillEB;
    /* 0xEC */ bool8 muzzledStatus;
    /* 0xED */ u8 muzzledTurnsLeft;
    u8 fillEE[0xF0 - 0xEE];
    /* 0xF0 */ bool8 radarStatus;
    /* 0xF1 */ bool8 scanningStatus;
    /* 0xF2 */ bool8 stairSpotterStatus;
    u8 fillF3;
    /* 0xF4 */ bool8 grudgeStatus;
    /* 0xF5 */ bool8 exposedStatus;
    u8 fillF7;
    /* 0xF7 */ bool8 isBoss;
    u8 fillF8[0xFA - 0xF8];
    /* 0xFA */ u8 terrifiedTurnsLeft; // Doubles as a bool for whether the Pokémon is terrified.
    u8 unkFB;
    // Set to true if the player makes a teammate use their held item.
    // This is done by going to the teammate's held item in the toolbox and selecting "Use".
    /* 0xFC */ bool8 useHeldItem;
    /* 0xFD */ u8 perishSongTimer; // When this reaches 0, the Pokémon faints from Perish Song. Doubles as a bool for whether the Pokémon is afflicted by Perish Song.
    u8 fillFE[0x100 - 0xFE];
    /* 0x100 */ u8 targetingDecoy; // If the Pokémon is targeting a decoy, this indicates whether the decoy target is a team or wild Pokémon.
    u8 fill101[0x104 - 0x101];
    /* 0x104 */ u8 movementSpeed;
    u8 fill105[0x108 - 0x105];
    // The turn counter for movement speed up/down is split into five timers each. Multiple timers are used if the Pokémon is affected by multiple
    // speed-up/slow effects at once, like using Agility twice.
    /* 0x108 */ u8 speedUpTurnsLeft[5];
    /* 0x10D */ u8 slowTurnsLeft[5];
    /* 0x112 */ u8 stockpileCount;
    u8 fill113;
    // When true, an AI Pokémon will move in a random direction every turn.
    // Unclear where this is set in-game; it is not set by statuses (e.g., confusion) or mission clients.
    /* 0x114 */ bool8 moveRandomly;
    u8 fill115[0x118 - 0x115];
    /* 0x118 */ struct PokemonMove moves[MAX_MON_MOVES];
    /* 0x138 */ u8 struggleMoveFlags;
    u8 fill139[0x13C - 0x139];
    /* 0x13C */ u32 belly;
    /* 0x140 */ u32 maxBelly;
    /* 0x144 */ bool8 movingIntoTarget; // True if an AI Pokémon is following another Pokémon and is already adjacent to them.
    /* 0x145 */ bool8 recalculateFollow; // Used by the AI to defer a movement decision until after all other Pokémon have moved.
    u8 fill146;
    /* 0x147 */ bool8 waiting; // True if an AI Pokémon decided to do nothing this turn.
    /* 0x148 */ bool8 attacking;
    u8 fill149[0x14E - 0x149];
    /* 0x14E */ u16 visualFlags;
    /* 0x150 */ u16 previousVisualFlags;
    /* 0x152 */ u8 unk152;
    u8 fill153[0x15C - 0x153];
    u8 unk15C;
    u8 unk15D;
    u8 unk15E;
    u8 unk15F;
    u8 fill160[0x16C - 0x160];
    /* 0x16C */ struct Position targetPosition;
    /* 0x170 */ struct Position posPixel;
    u32 unk174;
    u8 fill178[0x184 - 0x178];
    // Previous value of targetPosition for movement, 1 and 2 moves ago.
    /* 0x184 */ struct Position previousTargetMovePosition1;
    /* 0x188 */ struct Position32 previousTargetMovePosition2;
    /* 0x190 */ u8 lastMoveDirection; // The last direction that the Pokémon moved in.
    u8 fill191[0x194 - 0x191];
    // Number of tiles that the Pokémon moved last, multiplied by 0x100.
    /* 0x194 */ struct Position32 lastMoveIncrement;
    /* 0x19C */ u8 walkAnimationCounter; // Set when the Pokémon starts moving, and counts down until the Pokémon's walk animation stops.
    u8 fill19D[0x1F4 - 0x19D];
    /* 0x1F4 */ u8 numMoveTiles; // Number of tiles to move in a turn. Can be greater than 1 if the user's movement speed is boosted.
    u8 fill1F5;
    /* 0x1F6 */ bool8 notMoving;
    u8 fill1F7[0x1FA - 0x1F7];
    /* 0x1FA */ u8 mobileTurnTimer; // When a Pokémon can pass through walls in a hallway, this counts up to 200 before the Pokémon turns in a random direction.
    u8 fill1FB;
    /* 0x1FC */ u16 expGainedInTurn; // Used to accumulate experience when multiple enemies are defeated in one turn.
    u8 fill1FE[0x208 - 0x1FE];
};

// Used for Pokémon, items, and traps.
struct DungeonEntity
{
    /* 0x0 */ u32 entityType;
    /* 0x4 */ struct Position posWorld;
    /* 0x8 */ struct Position prevPosWorld;
    // The center of the entity acccording to pixel-space coordinates, using the same origin as posWorld.
    // X = (posWorld * 24 + 16) * 256, while Y = (posWorld * 24 + 12) * 256.
    /* 0xC */ struct Position32 posPixel;
    /* 0x14 */ struct Position32 prevPosPixel;
    u8 fill1C[0x20 - 0x1C];
    /* 0x20 */ bool8 visible; // Turned off when a Pokémon faints.
    u8 fill21[0x25 - 0x21];
    /* 0x25 */ u8 roomIndex;
    // The global spawn index counter starts at 10. Each Pokémon that spawns increments the counter and
    // gets assigned the current counter value as its spawn index.
    /* 0x26 */ u16 spawnIndex;
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
    u8 fill56[0x6A - 0x56];
    /* 0x6A */ u8 unk6A;
    /* 0x6A */ u8 unk6B;
    /* 0x6C */ u8 facingDir;
    /* 0x6D */ u8 facingDir2; // Duplicate of 0x6C?
    u8 fill6D[0x70 - 0x6E];
    /* 0x70 */ struct DungeonEntityData *entityData;
};

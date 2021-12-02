from Classes import *
from GameIDs import ChunkId

chunkLink = {0x0301B000: CCGameCtnCollectorList.Chunk000,

             0x03024000: CGameCtnMediaBlock3dStereo.Chunk000,

             0x03029001: CGameCtnMediaBlockTriangles.Chunk001,

             0x0303F005: CGameGhost.Chunk005,

             0x03043002: CGameCtnChallenge.Chunk002,
             0x03043003: CGameCtnChallenge.Chunk003,
             0x03043004: CGameCtnChallenge.Chunk004,
             0x03043005: CGameCtnChallenge.Chunk005,
             0x03043007: CGameCtnChallenge.Chunk007,
             0x0304300D: CGameCtnChallenge.Chunk00D,
             0x03043011: CGameCtnChallenge.Chunk011,
             0x03043017: CGameCtnChallenge.Chunk017,
             0x03043018: CGameCtnChallenge.Chunk018,
             0x03043019: CGameCtnChallenge.Chunk019,
             0x0304301C: CGameCtnChallenge.Chunk01C,
             0x0304301F: CGameCtnChallenge.Chunk01F,
             0x03043021: CGameCtnChallenge.Chunk021,
             0x03043022: CGameCtnChallenge.Chunk022,
             0x03043024: CGameCtnChallenge.Chunk024,
             0x03043025: CGameCtnChallenge.Chunk025,
             0x03043026: CGameCtnChallenge.Chunk026,
             0x03043028: CGameCtnChallenge.Chunk028,
             0x03043029: CGameCtnChallenge.Chunk029,
             0x0304302A: CGameCtnChallenge.Chunk02A,

             0x03059002: CGameCtnBlockSkin.Chunk002,

             0x0305B001: CGameCtnChallengeParameters.Chunk001,
             0x0305B004: CGameCtnChallengeParameters.Chunk004,
             0x0305B008: CGameCtnChallengeParameters.Chunk008,

             0x03078001: CGameCtnMediaTrack.Chunk001,
             0x03078004: CGameCtnMediaTrack.Chunk004,

             0x03079004: CGameCtnMediaClip.Chunk004,
             0x03079005: CGameCtnMediaClip.Chunk005,
             0x03079007: CGameCtnMediaClip.Chunk007,

             0x0307A003: CGameCtnMediaClipGroup.Chunk003,

             0x03080003: CGameCtnMediaBlockFxColors.Chunk003,

             0x03081001: CGameCtnMediaBlockFxBlurDepth.Chunk001,

             0x03082000: CGameCtnMediaBlockFxBlurMotion.Chunk000,

             0x03083001: CGameCtnMediaBlockFxBloom.Chunk001,

             0x03084003: CGameControlCameraFree.Chunk003,

             0x03085000: CGameCtnMediaBlockTime.Chunk000,

             0x03092005: CGameCtnGhost.Chunk005,
             0x03092008: CGameCtnGhost.Chunk008,
             0x03092009: CGameCtnGhost.Chunk009,
             0x0309200A: CGameCtnGhost.Chunk00A,
             0x0309200B: CGameCtnGhost.Chunk00B,
             0x0309200C: CGameCtnGhost.Chunk00C,
             0x0309200E: CGameCtnGhost.Chunk00E,
             0x0309200F: CGameCtnGhost.Chunk00F,
             0x03092010: CGameCtnGhost.Chunk010,
             0x03092012: CGameCtnGhost.Chunk012,
             0x03092013: CGameCtnGhost.Chunk013,
             0x03092014: CGameCtnGhost.Chunk014,
             0x03092015: CGameCtnGhost.Chunk015,
             0x03092017: CGameCtnGhost.Chunk017,
             0x03092018: CGameCtnGhost.Chunk018,
             0x03092019: CGameCtnGhost.Chunk019,

             0x03093000: CGameCtnReplayRecord.Chunk000,
             0x03093001: CGameCtnReplayRecord.Chunk001,
             0x03093002: CGameCtnReplayRecord.Chunk002,
             0x03093007: CGameCtnReplayRecord.Chunk007,
             0x03093014: CGameCtnReplayRecord.Chunk014,
             0x03093015: CGameCtnReplayRecord.Chunk015,

             0x030A1002: CGameCtnMediaBlockCameraPath.Chunk002,

             0x030A2005: CGameCtnMediaBlockCameraCustom.Chunk005,

             0x030A4000: CGameCtnMediaBlockCameraEffectShake.Chunk000,

             0x030A5000: CGameCtnMediaBlockImage.Chunk000,

             0x030A6001: CGameCtnMediaBlockMusicEffect.Chunk001,

             0x030A7001: CGameCtnMediaBlockSound.Chunk001,
             0x030A7002: CGameCtnMediaBlockSound.Chunk002,
             0x030A7003: CGameCtnMediaBlockSound.Chunk003,
             0x030A7004: CGameCtnMediaBlockSound.Chunk004,

             0x030A8001: CGameCtnMediaBlockText.Chunk001,
             0x030A8002: CGameCtnMediaBlockText.Chunk002,

             0x030A9000: CGameCtnMediaBlockTrails.Chunk000,

             0x030AB000: CGameCtnMediaBlockTransitionFade.Chunk000,

             0x030E5001: CGameCtnMediaBlockGhost.Chunk001,
             0x030E5002: CGameCtnMediaBlockGhost.Chunk002,

             0x07010003: CControlEffectSimi.Chunk003,
             0x07010005: CControlEffectSimi.Chunk005,

             0x0B005008: CSystemConfig.Chunk008,
             0x0B005009: CSystemConfig.Chunk009,
             0x0B00500B: CSystemConfig.Chunk00B,
             0x0B005020: CSystemConfig.Chunk020,
             0x0B00502B: CSystemConfig.Chunk02B,
             0x0B005030: CSystemConfig.Chunk030,
             0x0B005034: CSystemConfig.Chunk034,
             0x0B005039: CSystemConfig.Chunk039,
             0x0B00503A: CSystemConfig.Chunk03A,
             0x0B00503E: CSystemConfig.Chunk03E,
             0x0B005041: CSystemConfig.Chunk041,
             0x0B005044: CSystemConfig.Chunk044,
             0x0B005045: CSystemConfig.Chunk045,
             0x0B005047: CSystemConfig.Chunk047,
             0x0B005048: CSystemConfig.Chunk048,
             0x0B005049: CSystemConfig.Chunk049,
             0x0B00504A: CSystemConfig.Chunk04A,
             0x0B00504C: CSystemConfig.Chunk04C,
             0x0B00504D: CSystemConfig.Chunk04D,
             0x0B00504E: CSystemConfig.Chunk04E,
             0x0B00504F: CSystemConfig.Chunk04F,

             0x0B013001: CSystemConfigDisplay.Chunk001,
             0x0B013003: CSystemConfigDisplay.Chunk003,
             0x0B013004: CSystemConfigDisplay.Chunk004,
             0x0B013005: CSystemConfigDisplay.Chunk005,
             0x0B013008: CSystemConfigDisplay.Chunk008,
             0x0B013009: CSystemConfigDisplay.Chunk009,
             0x0B01300A: CSystemConfigDisplay.Chunk00A,
             0x0B01300B: CSystemConfigDisplay.Chunk00B,
             0x0B01300F: CSystemConfigDisplay.Chunk00F,
             0x0B013010: CSystemConfigDisplay.Chunk010,
             0x0B013011: CSystemConfigDisplay.Chunk011,
             0x0B013013: CSystemConfigDisplay.Chunk013,
             0x0B013015: CSystemConfigDisplay.Chunk015,
             0x0B013016: CSystemConfigDisplay.Chunk016,
             0x0B013017: CSystemConfigDisplay.Chunk017,
             0x0B013018: CSystemConfigDisplay.Chunk018,
             0x0B013019: CSystemConfigDisplay.Chunk019,
             0x0B01301B: CSystemConfigDisplay.Chunk01B,
             0x0B01301C: CSystemConfigDisplay.Chunk01C,
             0x0B01301D: CSystemConfigDisplay.Chunk01D,
             0x0B01301E: CSystemConfigDisplay.Chunk01E,
             0x0B013020: CSystemConfigDisplay.Chunk020,
             0x0B013021: CSystemConfigDisplay.Chunk021,
             0x0B013022: CSystemConfigDisplay.Chunk022}

skippableChunkList = {0x03043017,
                      0x03043018,
                      0x03043019,
                      0x0304301C,
                      0x03043029,
                      0x03092005,
                      0x03092008,
                      0x03092009,
                      0x0309200a,
                      0x0309200b,
                      0x03092013,
                      0x03092014,
                      0x03092017,
                      0x03093007,
                      0x0B005008,
                      0x0B005009,
                      0x0B00500B,
                      0x0B005020,
                      0x0B00502B,
                      0x0B005030,
                      0x0B005034,
                      0x0B005039,
                      0x0B00503A,
                      0x0B00503E,
                      0x0B005041,
                      0x0B005044,
                      0x0B005045,
                      0x0B005047,
                      0x0B005048,
                      0x0B005049,
                      0x0B00504A,
                      0x0B00504C,
                      0x0B00504D,
                      0x0B00504E,
                      0x0B00504F,

                      0x0B013001,
                      0x0B013003,
                      0x0B013004,
                      0x0B013005,
                      0x0B013008,
                      0x0B013009,
                      0x0B01300A,
                      0x0B01300B,
                      0x0B01300F,
                      0x0B013010,
                      0x0B013011,
                      0x0B013013,
                      0x0B013015,
                      0x0B013016,
                      0x0B013017,
                      0x0B013018,
                      0x0B013019,
                      0x0B01301B,
                      0x0B01301C,
                      0x0B01301D,
                      0x0B01301E,
                      0x0B013020,
                      0x0B013021,
                      0x0B013022
                      }


def is_known(id: ChunkId) -> bool:
    return id.value in chunkLink


def is_skippable(id: ChunkId) -> bool:
    return id.value in skippableChunkList

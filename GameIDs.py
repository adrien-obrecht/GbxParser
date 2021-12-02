from enum import Enum


class ChunkId(Enum):
    """
    Enum of the supported chunk ids (see https://wiki.xaseco.org/wiki/Class_IDs for more info)
    """
    CControlEffectSimi000 = 117506048
    CControlEffectSimi005 = 117506053
    CGameCtnBlockSkin000 = 50696192
    CGameCtnBlockSkin002 = 50696194
    CGameCtnChallenge000 = 50606080
    CGameCtnChallenge002 = 50606082
    CGameCtnChallenge003 = 50606083
    CGameCtnChallenge004 = 50606084
    CGameCtnChallenge005 = 50606085
    CGameCtnChallenge007 = 50606087
    CGameCtnChallenge00D = 50606093
    CGameCtnChallenge011 = 50606097
    CGameCtnChallenge017 = 50606103
    CGameCtnChallenge018 = 50606104
    CGameCtnChallenge019 = 50606105
    CGameCtnChallenge01C = 50606108
    CGameCtnChallenge01F = 50606111
    CGameCtnChallenge021 = 50606113
    CGameCtnChallenge022 = 50606114
    CGameCtnChallenge024 = 50606116
    CGameCtnChallenge025 = 50606117
    CGameCtnChallenge026 = 50606118
    CGameCtnChallenge028 = 50606120
    CGameCtnChallenge029 = 50606121
    CGameCtnChallenge02A = 50606122
    CGameCtnChallengeParameters000 = 50704384
    CGameCtnChallengeParameters001 = 50704385
    CGameCtnChallengeParameters004 = 50704388
    CGameCtnChallengeParameters008 = 50704392
    CGameCtnCollectorList000 = 50442240
    CGameCtnGhost000 = 50929664
    CGameCtnGhost005 = 50929669
    CGameCtnGhost008 = 50929672
    CGameCtnGhost009 = 50929673
    CGameCtnGhost00A = 50929674
    CGameCtnGhost00B = 50929675
    CGameCtnGhost00C = 50929676
    CGameCtnGhost00E = 50929678
    CGameCtnGhost00F = 50929679
    CGameCtnGhost010 = 50929680
    CGameCtnGhost012 = 50929682
    CGameCtnGhost013 = 50929683
    CGameCtnGhost014 = 50929684
    CGameCtnGhost015 = 50929685
    CGameCtnGhost017 = 50929687
    CGameCtnGhost018 = 50929688
    CGameCtnGhost019 = 50929689
    CGameCtnMediaBlockCameraCustom000 = 50995200
    CGameCtnMediaBlockCameraCustom005 = 50995205
    CGameCtnMediaBlockCameraGame000 = 50872320
    CGameCtnMediaBlockCameraGame003 = 50872323
    CGameCtnMediaBlockFxBlurMotion000 = 50864128
    CGameCtnMediaBlockGhost001 = 51269633
    CGameCtnMediaBlockGhost002 = 51269634
    CGameCtnMediaBlockText000 = 51019776
    CGameCtnMediaBlockText001 = 51019777
    CGameCtnMediaBlockText002 = 51019778
    CGameCtnMediaBlockTime000 = 50876416
    CGameCtnMediaBlockTrails000 = 51023872
    CGameCtnMediaBlockTransitionFade000 = 51032064
    CGameCtnMediaBlockTriangles001 = 50499585
    CGameCtnMediaClip000 = 50827264
    CGameCtnMediaClip004 = 50827268
    CGameCtnMediaClip005 = 50827269
    CGameCtnMediaClip007 = 50827271
    CGameCtnMediaClipGroup000 = 50831360
    CGameCtnMediaClipGroup003 = 50831363
    CGameCtnMediaTrack000 = 50823168
    CGameCtnMediaTrack001 = 50823169
    CGameCtnMediaTrack004 = 50823172
    CGameCtnReplayRecord000 = 50933760
    CGameCtnReplayRecord001 = 50933761
    CGameCtnReplayRecord002 = 50933762
    CGameCtnReplayRecord007 = 50933767
    CGameCtnReplayRecord014 = 50933780
    CGameCtnReplayRecord015 = 50933781
    CGameGhost005 = 50589701
    CSystemConfig008 = 184569864
    CSystemConfig009 = 184569865
    CSystemConfig00B = 184569867
    CSystemConfig020 = 184569888
    CSystemConfig02B = 184569899
    CSystemConfig030 = 184569904
    CSystemConfig034 = 184569908
    CSystemConfig039 = 184569913
    CSystemConfig03A = 184569914
    CSystemConfig03E = 184569918
    CSystemConfig041 = 184569921
    CSystemConfig044 = 184569924
    CSystemConfig045 = 184569925
    CSystemConfig047 = 184569927
    CSystemConfig048 = 184569928
    CSystemConfig049 = 184569929
    CSystemConfig04A = 184569930
    CSystemConfig04C = 184569932
    CSystemConfig04D = 184569933
    CSystemConfig04E = 184569934
    CSystemConfig04F = 184569935
    CSystemConfigDisplay001 = 184627201
    CSystemConfigDisplay003 = 184627203
    CSystemConfigDisplay004 = 184627204
    CSystemConfigDisplay005 = 184627205
    CSystemConfigDisplay008 = 184627208
    CSystemConfigDisplay009 = 184627209
    CSystemConfigDisplay00A = 184627210
    CSystemConfigDisplay00B = 184627211
    CSystemConfigDisplay00F = 184627215
    CSystemConfigDisplay010 = 184627216
    CSystemConfigDisplay011 = 184627217
    CSystemConfigDisplay013 = 184627219
    CSystemConfigDisplay015 = 184627221
    CSystemConfigDisplay016 = 184627222
    CSystemConfigDisplay017 = 184627223
    CSystemConfigDisplay018 = 184627224
    CSystemConfigDisplay019 = 184627225
    CSystemConfigDisplay01B = 184627227
    CSystemConfigDisplay01C = 184627228
    CSystemConfigDisplay01D = 184627229
    CSystemConfigDisplay01E = 184627230
    CSystemConfigDisplay020 = 184627232
    CSystemConfigDisplay021 = 184627233
    CSystemConfigDisplay022 = 184627234
    CTrackManiaReplayRecord000 = 604495872
    Facade = 0xFACADE01
    Skip = int.from_bytes(b'SKIP', 'big')
    Unknown = 1056968704

    @classmethod
    def intIsChunkId(cls, i: int) -> bool:
        """
        Returns whether the provided int is a known chunkId
        :param i: the integer that is tested
        :return: true if i is a known chunkId
        """
        return i in set(item.value for item in ChunkId)


class NodeId(Enum):
    """
    Enum of the supported node ids (see https://wiki.xaseco.org/wiki/Class_IDs for more info)
    """
    Body = 1
    CControlEffectSimi = 117506048
    CGameCtnBlockSkin = 50696192
    CGameCtnChallenge = 50606080
    CGameCtnChallengeParameters = 50704384
    CGameCtnCollectorList = 50442240
    CGameCtnGhost = 50929664
    CGameCtnMediaBlockCameraCustom = 50995200
    CGameCtnMediaBlockCameraGame = 50872320
    CGameCtnMediaBlockFxBlurMotion = 50864128
    CGameCtnMediaBlockGhost = 51269632
    CGameCtnMediaBlockText = 51019776
    CGameCtnMediaBlockTime = 50876416
    CGameCtnMediaBlockTrails = 51023872
    CGameCtnMediaBlockTransitionFade = 51032064
    CGameCtnMediaBlockTriangles2D = 50638848
    CGameCtnMediaClip = 50827264
    CGameCtnMediaClipGroup = 50831360
    CGameCtnMediaTrack = 50823168
    CGameCtnReplayRecord = 50933760
    CSystemConfig = 184569856
    CTrackManiaReplayRecord = 604495872
    Unknown = 1056968704

    @classmethod
    def intIsNodeId(cls, i: int) -> bool:
        """
        Returns whether the provided int is a known nodeId
        :param i: the integer that is tested
        :return: true if i is a known nodeId
        """
        return i in set(item.value for item in NodeId)

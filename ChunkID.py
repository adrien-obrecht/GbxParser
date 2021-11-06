from enum import Enum


class Id(Enum):
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
    CGameCtnChallenge00C = 50606093
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
    CGameCtnMediaBlockText000 = 51019776
    CGameCtnMediaBlockText001 = 51019777
    CGameCtnMediaBlockText002 = 51019778
    CGameCtnMediaBlockTrails000 = 51023872
    CGameCtnMediaBlockTransitionFade000 = 51032064
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
    CGameGhost005 = 50589701
    CTrackManiaReplayRecord000 = 604495872
    Facade = 4207599105
    Unknown = 1056968704

    @classmethod
    def intIsId(cls, i):
        return i in set(item.value for item in Id)

    @classmethod
    def strIsId(cls, s):
        return s in set(item.name for item in Id)

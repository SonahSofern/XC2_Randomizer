import json
import random
from IDs import Arts, AutoAttacks
import Options


EnhancementSets = [[2760, 2761, 2762, 2763, 2764, 2764], [2745, 2746, 2747, 2748, 2749, 2749], [2815, 2816, 2817, 2818, 2819, 2819], [2830, 2831, 2832, 2833, 2834, 2834], [2815, 2816, 2817, 2818, 2819, 2819], [2861, 2862, 2863, 2864, 2865, 2865], [2745, 2746, 2747, 2748, 2749, 2749], [2815, 2816, 2817, 2818, 2819, 2819], [2680, 2681, 2682, 2683, 2684, 2684], [2815, 2816, 2817, 2818, 2819, 2819], [2746, 2746, 2746, 2746, 2746, 2746], [2815, 2816, 2817, 2818, 2819, 2819], [2680, 2681, 2682, 2683, 2684, 2684], [2680, 2681, 2682, 2683, 2684, 2684], [2815, 2816, 2817, 2818, 2819, 2819], [2700, 2701, 2702, 2703, 2704, 2704], [2755, 2756, 2757, 2758, 2759, 2759], [2780, 2781, 2782, 2783, 2784, 2784], [2790, 2791, 2792, 2793, 2794, 2794], [2855, 2856, 2857, 2858, 2859, 2859], [2795, 2796, 2797, 2798, 2799, 2799], [2866, 2866, 2866, 2866, 2866, 2866], [2770, 2771, 2772, 2773, 2774, 2774], [2735, 2736, 2737, 2738, 2739, 2739], [2765, 2766, 2767, 2768, 2769, 2769], [2790, 2791, 2792, 2793, 2794, 2794], [2850, 2851, 2852, 2853, 2854, 2854], [2866, 2866, 2866, 2866, 2866, 2866], [2765, 2766, 2767, 2768, 2769, 2769], [2850, 2851, 2852, 2853, 2854, 2854], [2866, 2866, 2866, 2866, 2866, 2866], [2770, 2771, 2772, 2773, 2774, 2774], [2725, 2726, 2727, 2728, 2729, 2729], [2740, 2741, 2742, 2743, 2744, 2744], [2725, 2726, 2727, 2728, 2729, 2729], [2770, 2771, 2772, 2773, 2774, 2774], [2790, 2791, 2792, 2793, 2794, 2794], [2825, 2826, 2827, 2828, 2829, 2829], [2700, 2701, 2702, 2703, 2704, 2704], [2790, 2791, 2792, 2793, 2794, 2794], [2825, 2826, 2827, 2828, 2829, 2829], [2700, 2701, 2702, 2703, 2704, 2704], [2770, 2771, 2772, 2773, 2774, 2774], [2705, 2706, 2707, 2708, 2709, 2709], [2840, 2841, 2842, 2843, 2844, 2844], [2840, 2841, 2842, 2843, 2844, 2844], [2765, 2766, 2767, 2768, 2769, 2769], [2705, 2706, 2707, 2708, 2709, 2709], [2705, 2706, 2707, 2708, 2709, 2709], [2840, 2841, 2842, 2843, 2844, 2844], [2775, 2776, 2777, 2778, 2779, 2779], [2765, 2766, 2767, 2768, 2769, 2769], [2840, 2841, 2842, 2843, 2844, 2844], [2800, 2801, 2802, 2803, 2804, 2804], [2745, 2746, 2747, 2748, 2749, 2749], [2830, 2831, 2832, 2833, 2834, 2834], [2685, 2686, 2687, 2688, 2689, 2689], [2800, 2801, 2802, 2803, 2804, 2804], [2685, 2686, 2687, 2688, 2689, 2689], [2760, 2761, 2762, 2763, 2764, 2764], [2830, 2831, 2832, 2833, 2834, 2834], [2760, 2761, 2762, 2763, 2764, 2764], [2800, 2801, 2802, 2803, 2804, 2804], [2830, 2831, 2832, 2833, 2834, 2834], [2750, 2751, 2752, 2753, 2754, 2754], [2760, 2761, 2762, 2763, 2764, 2764], [2830, 2831, 2832, 2833, 2834, 2834], [2805, 2806, 2807, 2808, 2809, 2809], [2861, 2862, 2863, 2864, 2865, 2865], [2810, 2811, 2812, 2813, 2814, 2814], [2810, 2811, 2812, 2813, 2814, 2814], [2861, 2862, 2863, 2864, 2865, 2865], [2780, 2781, 2782, 2783, 2784, 2784], [2805, 2806, 2807, 2808, 2809, 2809], [2861, 2862, 2863, 2864, 2865, 2865], [2805, 2806, 2807, 2808, 2809, 2809], [2780, 2781, 2782, 2783, 2784, 2784], [2861, 2862, 2863, 2864, 2865, 2865], [2810, 2811, 2812, 2813, 2814, 2814], [2780, 2781, 2782, 2783, 2784, 2784], [2850, 2851, 2852, 2853, 2854, 2854], [2740, 2741, 2742, 2743, 2744, 2744], [2770, 2771, 2772, 2773, 2774, 2774], [2740, 2741, 2742, 2743, 2744, 2744], [2850, 2851, 2852, 2853, 2854, 2854], [2770, 2771, 2772, 2773, 2774, 2774], [2850, 2851, 2852, 2853, 2854, 2854], [2770, 2771, 2772, 2773, 2774, 2774], [2780, 2781, 2782, 2783, 2784, 2784], [2785, 2786, 2787, 2788, 2789, 2789], [2850, 2851, 2852, 2853, 2854, 2854], [2795, 2796, 2797, 2798, 2799, 2799], [2866, 2866, 2866, 2866, 2866, 2866], [2715, 2716, 2717, 2718, 2719, 2719], [2866, 2866, 2866, 2866, 2866, 2866], [2795, 2796, 2797, 2798, 2799, 2799], [2850, 2851, 2852, 2853, 2854, 2854], [2866, 2866, 2866, 2866, 2866, 2866], [2795, 2796, 2797, 2798, 2799, 2799], [2850, 2851, 2852, 2853, 2854, 2854], [2866, 2866, 2866, 2866, 2866, 2866], [2740, 2741, 2742, 2743, 2744, 2744], [2850, 2851, 2852, 2853, 2854, 2854], [2795, 2796, 2797, 2798, 2799, 2799], [2815, 2816, 2817, 2818, 2819, 2819], [2765, 2766, 2767, 2768, 2769, 2769], [2845, 2846, 2847, 2848, 2849, 2849], [2775, 2776, 2777, 2778, 2779, 2779], [2815, 2816, 2817, 2818, 2819, 2819], [2765, 2766, 2767, 2768, 2769, 2769], [2815, 2816, 2817, 2818, 2819, 2819], [2775, 2776, 2777, 2778, 2779, 2779], [2800, 2801, 2802, 2803, 2804, 2804], [2755, 2756, 2757, 2758, 2759, 2759], [2765, 2766, 2767, 2768, 2769, 2769], [2845, 2846, 2847, 2848, 2849, 2849], [2815, 2816, 2817, 2818, 2819, 2819], [2810, 2811, 2812, 2813, 2814, 2814], [2815, 2816, 2817, 2818, 2819, 2819], [2755, 2756, 2757, 2758, 2759, 2759], [2810, 2811, 2812, 2813, 2814, 2814], [2815, 2816, 2817, 2818, 2819, 2819], [2745, 2746, 2747, 2748, 2749, 2749], [2810, 2811, 2812, 2813, 2814, 2814], [2815, 2816, 2817, 2818, 2819, 2819], [2745, 2746, 2747, 2748, 2749, 2749], [2755, 2756, 2757, 2758, 2759, 2759], [2815, 2816, 2817, 2818, 2819, 2819], [2830, 2831, 2832, 2833, 2834, 2834], [2760, 2761, 2762, 2763, 2764, 2764], [2745, 2746, 2747, 2748, 2749, 2749], [2830, 2831, 2832, 2833, 2834, 2834], [2860, 2860, 2860, 2860, 2860, 2860], [2760, 2761, 2762, 2763, 2764, 2764], [2861, 2862, 2863, 2864, 2865, 2865], [2740, 2741, 2742, 2743, 2744, 2744], [2805, 2806, 2807, 2808, 2809, 2809], [2760, 2761, 2762, 2763, 2764, 2764], [2845, 2846, 2847, 2848, 2849, 2849], [2830, 2831, 2832, 2833, 2834, 2834], [2815, 2816, 2817, 2818, 2819, 2819], [2815, 2816, 2817, 2818, 2819, 2819], [2845, 2846, 2847, 2848, 2849, 2849], [2830, 2831, 2832, 2833, 2834, 2834], [2845, 2846, 2847, 2848, 2849, 2849], [2815, 2816, 2817, 2818, 2819, 2819], [2830, 2831, 2832, 2833, 2834, 2834], [2830, 2831, 2832, 2833, 2834, 2834], [2845, 2846, 2847, 2848, 2849, 2849], [2815, 2816, 2817, 2818, 2819, 2819], [2790, 2791, 2792, 2793, 2794, 2794], [2745, 2746, 2747, 2748, 2749, 2749], [2825, 2826, 2827, 2828, 2829, 2829], [2685, 2686, 2687, 2688, 2689, 2689], [2790, 2791, 2792, 2793, 2794, 2794], [2685, 2686, 2687, 2688, 2689, 2689], [2760, 2761, 2762, 2763, 2764, 2764], [2825, 2826, 2827, 2828, 2829, 2829], [2760, 2761, 2762, 2763, 2764, 2764], [2790, 2791, 2792, 2793, 2794, 2794], [2825, 2826, 2827, 2828, 2829, 2829], [2750, 2751, 2752, 2753, 2754, 2754], [2760, 2761, 2762, 2763, 2764, 2764], [2825, 2826, 2827, 2828, 2829, 2829], [2740, 2741, 2742, 2743, 2744, 2744], [2795, 2796, 2797, 2798, 2799, 2799], [2680, 2681, 2682, 2683, 2684, 2684], [2850, 2851, 2852, 2853, 2854, 2854], [2795, 2796, 2797, 2798, 2799, 2799], [2740, 2741, 2742, 2743, 2744, 2744], [2795, 2796, 2797, 2798, 2799, 2799], [2680, 2681, 2682, 2683, 2684, 2684], [2740, 2741, 2742, 2743, 2744, 2744], [2680, 2681, 2682, 2683, 2684, 2684], [2795, 2796, 2797, 2798, 2799, 2799], [2850, 2851, 2852, 2853, 2854, 2854], [2740, 2741, 2742, 2743, 2744, 2744], [2745, 2746, 2747, 2748, 2749, 2749], [2810, 2811, 2812, 2813, 2814, 2814], [2840, 2841, 2842, 2843, 2844, 2844], [2840, 2841, 2842, 2843, 2844, 2844], [2810, 2811, 2812, 2813, 2814, 2814], [2746, 2746, 2746, 2746, 2746, 2746], [2810, 2811, 2812, 2813, 2814, 2814], [2840, 2841, 2842, 2843, 2844, 2844], [2840, 2841, 2842, 2843, 2844, 2844], [2810, 2811, 2812, 2813, 2814, 2814], [2700, 2701, 2702, 2703, 2704, 2704], [2755, 2756, 2757, 2758, 2759, 2759], [2805, 2806, 2807, 2808, 2809, 2809], [2861, 2862, 2863, 2864, 2865, 2865], [2740, 2741, 2742, 2743, 2744, 2744], [2740, 2741, 2742, 2743, 2744, 2744], [2861, 2862, 2863, 2864, 2865, 2865], [2780, 2781, 2782, 2783, 2784, 2784], [2805, 2806, 2807, 2808, 2809, 2809], [2861, 2862, 2863, 2864, 2865, 2865], [2805, 2806, 2807, 2808, 2809, 2809], [2780, 2781, 2782, 2783, 2784, 2784], [2861, 2862, 2863, 2864, 2865, 2865], [2740, 2741, 2742, 2743, 2744, 2744], [2780, 2781, 2782, 2783, 2784, 2784], [2740, 2741, 2742, 2743, 2744, 2744], [2795, 2796, 2797, 2798, 2799, 2799], [2850, 2851, 2852, 2853, 2854, 2854], [2740, 2741, 2742, 2743, 2744, 2744], [2795, 2796, 2797, 2798, 2799, 2799], [2850, 2851, 2852, 2853, 2854, 2854], [2740, 2741, 2742, 2743, 2744, 2744], [2795, 2796, 2797, 2798, 2799, 2799], [2850, 2851, 2852, 2853, 2854, 2854], [2740, 2741, 2742, 2743, 2744, 2744], [2795, 2796, 2797, 2798, 2799, 2799], [2850, 2851, 2852, 2853, 2854, 2854], [2785, 2786, 2787, 2788, 2789, 2789], [2795, 2796, 2797, 2798, 2799, 2799], [2850, 2851, 2852, 2853, 2854, 2854], [2785, 2786, 2787, 2788, 2789, 2789], [2795, 2796, 2797, 2798, 2799, 2799], [2850, 2851, 2852, 2853, 2854, 2854], [2785, 2786, 2787, 2788, 2789, 2789], [2795, 2796, 2797, 2798, 2799, 2799], [2850, 2851, 2852, 2853, 2854, 2854], [2785, 2786, 2787, 2788, 2789, 2789], [2795, 2796, 2797, 2798, 2799, 2799], [2850, 2851, 2852, 2853, 2854, 2854], [2830, 2831, 2832, 2833, 2834, 2834], [2760, 2761, 2762, 2763, 2764, 2764], [2770, 2771, 2772, 2773, 2774, 2774], [2730, 2731, 2732, 2733, 2734, 2734], [2830, 2831, 2832, 2833, 2834, 2834], [2770, 2771, 2772, 2773, 2774, 2774], [2760, 2761, 2762, 2763, 2764, 2764], [2830, 2831, 2832, 2833, 2834, 2834], [2770, 2771, 2772, 2773, 2774, 2774], [2730, 2731, 2732, 2733, 2734, 2734], [2830, 2831, 2832, 2833, 2834, 2834], [2730, 2731, 2732, 2733, 2734, 2734], [2800, 2801, 2802, 2803, 2804, 2804], [2815, 2816, 2817, 2818, 2819, 2819], [2810, 2811, 2812, 2813, 2814, 2814], [2840, 2841, 2842, 2843, 2844, 2844], [2800, 2801, 2802, 2803, 2804, 2804], [2815, 2816, 2817, 2818, 2819, 2819], [2840, 2841, 2842, 2843, 2844, 2844], [2815, 2816, 2817, 2818, 2819, 2819], [2810, 2811, 2812, 2813, 2814, 2814], [2840, 2841, 2842, 2843, 2844, 2844], [2810, 2811, 2812, 2813, 2814, 2814], [2815, 2816, 2817, 2818, 2819, 2819], [2840, 2841, 2842, 2843, 2844, 2844], [2800, 2801, 2802, 2803, 2804, 2804], [2810, 2811, 2812, 2813, 2814, 2814], [2835, 2836, 2837, 2838, 2839, 2839], [2860, 2860, 2860, 2860, 2860, 2860], [2760, 2761, 2762, 2763, 2764, 2764], [2745, 2746, 2747, 2748, 2749, 2749], [2861, 2862, 2863, 2864, 2865, 2865], [2765, 2766, 2767, 2768, 2769, 2769], [2878, 2879, 2880, 2881, 2882, 2882], [3015, 3016, 3017, 3018, 3019, 3019], [2740, 2741, 2742, 2743, 2744, 2744], [2770, 2771, 2772, 2773, 2774, 2774], [2975, 2976, 2977, 2978, 2979, 2979], [2810, 2811, 2812, 2813, 2814, 2814], [2825, 2826, 2827, 2828, 2829, 2829], [2800, 2801, 2802, 2803, 2804, 2804], [2830, 2831, 2832, 2833, 2834, 2834], [2872, 2872, 2872, 2872, 2872, 2872], [2873, 2874, 2875, 2876, 2877, 2877], [2795, 2796, 2797, 2798, 2799, 2799], [2873, 2874, 2875, 2876, 2877, 2877], [2780, 2781, 2782, 2783, 2784, 2784], [2790, 2791, 2792, 2793, 2794, 2794], [2873, 2874, 2875, 2876, 2877, 2877], [2873, 2874, 2875, 2876, 2877, 2877], [2872, 2872, 2872, 2872, 2872, 2872], [2795, 2796, 2797, 2798, 2799, 2799], [2805, 2806, 2807, 2808, 2809, 2809], [2872, 2872, 2872, 2872, 2872, 2872], [2755, 2756, 2757, 2758, 2759, 2759], [2810, 2811, 2812, 2813, 2814, 2814], [2745, 2746, 2747, 2748, 2749, 2749], [2866, 2866, 2866, 2866, 2866, 2866], [2866, 2866, 2866, 2866, 2866, 2866], [2810, 2811, 2812, 2813, 2814, 2814], [2755, 2756, 2757, 2758, 2759, 2759], [2810, 2811, 2812, 2813, 2814, 2814], [2866, 2866, 2866, 2866, 2866, 2866], [2755, 2756, 2757, 2758, 2759, 2759], [2755, 2756, 2757, 2758, 2759, 2759], [2810, 2811, 2812, 2813, 2814, 2814], [2745, 2746, 2747, 2748, 2749, 2749], [2866, 2866, 2866, 2866, 2866, 2866], [2740, 2741, 2742, 2743, 2744, 2744], [2850, 2851, 2852, 2853, 2854, 2854], [2795, 2796, 2797, 2798, 2799, 2799], [2866, 2866, 2866, 2866, 2866, 2866], [2740, 2741, 2742, 2743, 2744, 2744], [2866, 2866, 2866, 2866, 2866, 2866], [2795, 2796, 2797, 2798, 2799, 2799], [2850, 2851, 2852, 2853, 2854, 2854], [2740, 2741, 2742, 2743, 2744, 2744], [2866, 2866, 2866, 2866, 2866, 2866], [2795, 2796, 2797, 2798, 2799, 2799], [2850, 2851, 2852, 2853, 2854, 2854], [2866, 2866, 2866, 2866, 2866, 2866], [2740, 2741, 2742, 2743, 2744, 2744], [2850, 2851, 2852, 2853, 2854, 2854], [2795, 2796, 2797, 2798, 2799, 2799]]


def DriverArtRandomizer():
    with open("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", 'r+', encoding='utf-8') as artFile:
        artData = json.load(artFile)
        
        isAutoAttacks = Options.DriverArtsOption_AutoAttacks.GetState()
        isMultiReact = Options.DriverArtsOption_MultipleReactions.GetState()
        isReactions = Options.DriverArtsOption_SingleReaction.GetState()
        isCooldowns = Options.DriverArtsOption_Cooldown.GetState()
        isDamage = Options.DriverArtsOption_Damage.GetState()
        isEnhancements = Options.DriverArtsOption_Enhancements.GetState()
        isBuffs = Options.DriverArtsOption_Buffs.GetState()
        isDebuffs = Options.DriverArtsOption_Debuffs.GetState()
        isAOE = Options.DriverArtsOption_AOE.GetState()
        isSpeed = Options.DriverArtsOption_AnimationSpeed.GetState()
        odds = Options.DriverArtsOption.GetOdds()
        
        for art in artData["rows"]:
            if (not isAutoAttacks) and (isAutoAttacks or (art["$id"] in AutoAttacks)): # Ignore auto attacks unless the option is clicked
                continue
            isEnemyTarget = (art["Target"] in [0,4]) # Ensures Targeting Enemy
    
            if (isReactions or isMultiReact) and isEnemyTarget:
                for i in range(1,17):
                    art[f"ReAct{i}"] = 0 # Clearing Defaults these are needed bc torna arts are weird so i cant clear them blindly before hand gotta follow these conditions so this is the easiest way
                if OddCheck(odds):
                    Reaction(art, isMultiReact)
                    
            if isCooldowns and OddCheck(odds):
                Cooldowns(art)
                
            if isDamage and OddCheck(odds):
                Damage(art)
                
            if isEnhancements and isEnemyTarget:
                for i in range(1,7):
                    art[f"Enhance{i}"] = 0
                if OddCheck(odds):
                    Enhancements(art)
                    
            if isBuffs:
                art["ArtsBuff"] = 0 
                if OddCheck(odds//2): # These are really strong so im lowering the odds
                    Buffs(art)
                    
            if isDebuffs and isEnemyTarget:
                art["ArtsDeBuff"] = 0
                if OddCheck(odds):
                    Debuffs(art)
                    
            if isAOE and isEnemyTarget:
                art["RangeType"] = 0
                if OddCheck(odds):
                    AOE(art)
                    
            if isSpeed and OddCheck(odds):
                AnimationSpeed(art)
            
        artFile.seek(0)
        artFile.truncate()
        json.dump(artData, artFile, indent=2, ensure_ascii=False)
 
def OddCheck(odds):
    return (odds > random.randrange(0,100))

def Reaction(art, multReact):
    ValidReactions = {
        "Break" : [1],
        "Topple": [2],
        "Launch": [3],
        "Smash": [4],
        "KB": [5,6,7,8,9],
        "BD": [10,11,12,13,14],
    }
    for i in range(1,17):
        name,values = random.choice(list(ValidReactions.items()))
        if art[f"HitFrm{i}"] == 0: # Make sure there is a hit
            art[f"ReAct{i-1}"] = random.choice(values) # Adds something to the last hit
            break
        if multReact:
            art[f"ReAct{i}"] =  random.choice(values) # Adds each hit

def Cooldowns(art): 
    CD = random.randrange(7,13)
    for i in range(1,7):
        step = random.choice([0,0,0,1,1,2])
        if CD > step:
            CD -= step
        art[f"Recast{i}"] = CD

def Damage(art): 
    DMG = random.randrange(100,200,10)
    for i in range(1,7):
        step = random.choice([0,0,30,30,50,50,100])
        DMG += step
        art[f"DmgMgn{i}"] = DMG
        
def Enhancements(art): 
    Enhancement = random.choice(EnhancementSets)
    for i in range(1,7):
        art[f"Enhance{i}"] = Enhancement[i-1]

def Buffs(art):
    Buffs = {
        "NlReact": 1,
        "Evade": 2,
        "Block": 3,
        "Counter": 6,
        "↑Counter": 7,
        "Rflct": 5,
        "Inv": 4,
        "Absorb":  17
        # Eventually might add logic for damage absorb and release
    }
    name, buff = random.choice(list(Buffs.items()))
    art["ArtsBuff"] = buff

def Debuffs(art):
    Debuffs = {
        "Taunt" : 11,
        # "Stench": 12,
        "NlHeal": 15,
        "Shackle": 14,
        "Def↓": 23,
        "EDef↓": 24,
        "Res↓": 25,
        # "Monado Armor": 16,
        # "Doom": 21,
        # "Superstrength": 17
    }
    name, debuff = random.choice(list(Debuffs.items()))
    art["ArtsDeBuff"] = debuff

def AnimationSpeed(art):
    art["ActSpeed"] = random.randrange(50,200,10)

def AOE(art):
    CircleAroundTarget = 1
    ConeAhead = 2
    CircleAroundUser = 5
    RangeType = random.choice([CircleAroundTarget, ConeAhead, CircleAroundUser])
    RandomRadius = random.randint(10,15)
    RandomLength = random.randrange(2,17,4)
    art["RangeType"] = RangeType
    art["Radius"] =  RandomRadius
    art["Length"] = RandomLength

def GenCustomArtDescriptions():
    RangeType = {
        "AOE" : [1,2,3,5]
    }

    MoveType = {
        "Heal": [3],
        "Defend": [11]
    }

    Reactions = {
        "B" : [1],
        "T" : [2],
        "L" : [3],
        "S" : [4],
        "Kb": [5,6,7,8,9],
        "Bd": [10,11,12,13,14]
    }

    FullReactions = {
        "Break" : [1],
        "Topple" : [2],
        "Launch" : [3],
        "Smash" : [4],
        "Knockback": [5,6,7,8,9],
        "Blowdown": [10,11,12,13,14]
    }

    Enhancements = {
        "Aggro↓" : [2830,2835],
        "Aggro↑" : [2850,2873],
        "Aggroed↑": [2795],
        "Aquatic↑": [2705],
        "Back↑": [2760,2755],
        "Cancel↑": [2810],
        "Crit↑": [2975],
        "Crit CD↓": [2840],
        "Evade": [2825,2866,2872],
        "Flying↑": [2700],
        "Front↑": [2740],
        "Vamp": [2735,2878],
        "Party Vamp": [2845],
        "High HP↑": [2800,2805],
        "HP Potion": [2815,2860],
        "Insect↑": [2685],
        "Launch↑": [2780,2775],
        "Low HP↑": [2790,2785],
        "Machine↑": [2730,2725],
        "Pierce": [2861],
        "Side↑": [2746,2745,2750],
        "Topple↑": [2770,2765],
        "Beast↑": [2680],
        "Humanoid↑": [2715]
    }

    Debuffs = {
        "Foe Crit↑": [1],
        "Foe Acc↑": [2],
        "Foe Art↑": [3],
        "Foe CD↓": [4],
        "Foe Shield": [5],
        "Foe Null React": [6],
        "Foe -Debuff": [7],
        "Foe Back↑": [8],
        "Foe Armor": [16],
        "Foe Atk↑": [17],
        "Taunt": [11],
        "Stench": [12], 
        "Shackle Dr": [13],
        "Shackle Bl": [14],
        "Null Heal": [15],
        "Doom": [21],
        "P Def↓": [23],
        "E Def↓": [24],
        "Res↓": [25],
        "Freeze": [30],
        "Enrage": [35]
    }
    Buffs = {
        "NlReact": [1],
        "Evade": [2],
        "Block": [3],
        "Counter": [6],
        "↑Counter": [7],
        "Reflect": [5],
        "Invincible": [4],
        "Absorb":  [17]
        # Eventually might add logic for damage absorb and release
    }
    
    with open("./_internal/JsonOutputs/common/BTL_Arts_Dr.json", "r+", encoding='utf-8') as ArtsFile:     
        with open("./_internal/JsonOutputs/common_ms/btl_arts_dr_cap.json", "r+", encoding='utf-8') as DescFile:     
            artsData = json.load(ArtsFile)
            descData = json.load(DescFile)
            AnchorShotDesc = 0
            
            for art in artsData["rows"]:
                if art["$id"] in Arts:

                    CurrDesc = art["Caption"]
                    CombinedCaption = ["","","","",""]
                    FirstDescriptionMod = 0
                    LastDescriptionMod = 0
                    # AOE
                    for key,values in RangeType.items():    
                        if art["RangeType"] in values:
                            CombinedCaption[0] += f"[System:Color name=blue]{key}[/System:Color]"
                            break

                    # Type of Art Not changing this currently 
                    # for key,values in MoveType.items():
                    #     if art["ArtsType"] in values:
                    #         CombinedCaption[1] += f"{key}"
                    #         break
                    
                    for key,values in Buffs.items():
                        if art["ArtsBuff"] in values:
                            CombinedCaption[1] += f"{key}"
                            break

                    # Reactions 
                    ReactCaption = ""
                    TypeReactions = []
                    for i in range(1,17):              
                        if art[f"HitDirID{i}"] != 0:
                            for key,values in Reactions.items():
                                if art[f"ReAct{i}"] in values:
                                    ReactCaption += f"[System:Color name=tutorial]{key}[/System:Color]->"
                                    TypeReactions.append(art[f"ReAct{i}"])
                                    break
                    ReactCaption = ReactCaption[:-2]
                    # if len(ReactCaption) > 15: # If the length is too long, shorten it to "Driver Combo"
                    #     ReactCaption = "[System:Color name=tutorial]Driver Combo[/System:Color]"
                    if len(TypeReactions) == 1: # If the length is 1, spell out the reaction
                        for key,values in FullReactions.items():
                            if TypeReactions[0] in values:
                                ReactCaption = f"[System:Color name=tutorial]{key}[/System:Color]"
                                break
                    CombinedCaption[2] = ReactCaption
                        
                    # Enhancements
                    for key,values in Enhancements.items():
                        if art["Enhance1"] in values:
                            CombinedCaption[3] += f"[System:Color name=green]{key}[/System:Color]"
                            break
                        
                    # Debuffs                       
                    for key,values in Debuffs.items():
                        if art["ArtsDeBuff"] in values:
                            CombinedCaption[4] = f"[System:Color name=red]{key}[/System:Color]"
                            break

                    # Putting it all together
                    TotalArtDescription = ""    
                    for i in range(0, len(CombinedCaption)):
                        if CombinedCaption[i] != "":
                            FirstDescriptionMod = i
                            break
                    for i in range(len(CombinedCaption) - 1, 0, -1):
                        if CombinedCaption[i] != "":
                            LastDescriptionMod = i
                            break
                    TotalArtDescription += CombinedCaption[FirstDescriptionMod]
                    if FirstDescriptionMod != LastDescriptionMod:
                        for i in range(FirstDescriptionMod + 1, LastDescriptionMod + 1):
                            if CombinedCaption[i] != "":
                                TotalArtDescription += " / "
                                TotalArtDescription += CombinedCaption[i]

                    if TotalArtDescription == "":
                        TotalArtDescription = "No Effects"

                    # Update Descriptions
                    for desc in descData["rows"]:
                        if desc["$id"] == CurrDesc:
                            desc["name"] = TotalArtDescription
                            break

            for desc in descData["rows"]:
                if desc["$id"] == 4:
                    AnchorShotDesc = desc["name"]
                    break
            for desc in descData["rows"]:
                if desc["$id"] == 5:
                    desc["name"] = AnchorShotDesc
                    break
            DescFile.seek(0)
            DescFile.truncate()
            json.dump(descData, DescFile, indent=2, ensure_ascii=False)             
        ArtsFile.seek(0)
        ArtsFile.truncate()
        json.dump(artsData, ArtsFile, indent=2, ensure_ascii=False)
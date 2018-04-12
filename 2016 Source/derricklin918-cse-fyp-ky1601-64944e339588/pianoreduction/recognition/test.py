from pianoreduction.recognition.eventanalysis.eventstatistics import EventStatistics

dataset = ["canon_in_D_excerpt_1.xml", "canon_in_D_excerpt_2.xml", "canon_in_D_excerpt_3.xml", "canon_in_D_excerpt_4.xml", "hoppipolla_excerpt.xml","moonlight_sonata_I_excerpt.xml", "SQ-Original-fixed.xml"]

if __name__ == "__main__":
    stats = EventStatistics(dataset)
    stats.run()
    stats.print_result()
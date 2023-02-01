def make_nut_file(mouse_id, celltype, path, inputdir, **kwargs):
    filename = "{}/{}_{}.nut".format(path, mouse_id, celltype)

    nutil_dict = {"type": "Quantifier",
                  "name": "{}_{}".format(mouse_id, celltype),
                  "analysis_type": "QUINT",
                  "quantifier_input_dir": "{}/{}".format(path, inputdir),
                  "quantifier_atlas_dir": "{}/Atlas".format(path),
                  "label_file": "Allen Mouse Brain 2017",
                  "custom_label_file": "",
                  "xml_anchor_file": "{}/lowres/{}.json".format(path, mouse_id),
                  "quantifier_output_dir": "{}/nutil_{}".format(path, celltype),
                  "output_report": "All",
                  "extraction_color": "255,255,255,255",
                  "object_splitting": "No",
                  "object_min_size": "10",
                  "global_pixel_scale": "1",
                  "quantifier_pixel_scale_unit": "pixels",
                  "use_custom_masks": "No",
                  "custom_mask_directory": "",
                  "custom_mask_color": "255,255,255,255",
                  "output_report_type": "CSV",
                  "custom_region_type": "Default",
                  "custom_region_file": "",
                  "coordinate_extraction": "All",
                  "coordinate_random_distortion": "0",
                  "pixel_density": "1",
                  "nifti_size": "0",
                  "display_label_id": "No",
                  "output_region_id": "Yes",
                  "pattern_match": "_sXXX",
                  "files": "",
                  "nutil_version": "v0.7.0"}

    with open(filename, "w") as f:
        for key, val in nutil_dict.items():
            f.write("{} = {}\n".format(key, val))

mouse_id = "FT136"
celltype = "coloc"
path = "D:/Test Data/fostrap/{}".format(mouse_id)
inputdir = "chan_coloc" # "chan2/nutil" or "chan3/nutil"

make_nut_file(mouse_id, celltype, path, inputdir)
#!/usr/bin/env python3.7
import io
import xlrd
import fire
from timecode import Timecode


def get_comment_duration(tc1_in, tc2_in, fps):
    tc1 = Timecode(fps, tc1_in)
    tc2 = Timecode(fps, tc2_in)
    tc1a = tc1 + Timecode(fps, "00:00:00:00")
    tc2a = tc2 + Timecode(fps, "00:00:00:00")
    duration_frames = str((tc2 - tc1).frames)
    durations = {"tc1": str(tc1), "tc2": str(tc2), "tc1a": str(tc1a), "tc2a": str(tc2a), "duration_frames": duration_frames}
    return durations


def main(file_in, file_out, fps="23.98", "ascii"):
    """ Convert an Excel spreadsheet with in/out TC to a compatible DaVinci Resolve EDL
    :param file_in: Path to Excel file (make sure the sheet is named 'Sheet1')
    :param file_out: Output edl name (make sure to use the .edl extension)
    :param fps: Frame rate. If not specified, defaults to 23.98. Supports 23.98, 24, 25, 29.97, 30, 50, 59.94,
    and 60 fps
    :return: EDL file
    """
    accepted_fps = ("23.98", "24", "25", "29.97", "30", "50", "59.97", "60")
    if fps in accepted_fps:
        try:
            try:
                x1 = xlrd.open_workbook(file_in, file_out)
                sheet = x1.sheet_by_name("Sheet1")
                print("Excel sheet opened...")
            except Exception as e:
                print("Problem opening sheet. Expecting sheet name 'Sheet1'")
                print(e)
            with io.open(file_out, "w") as file_out:
                file_out.write("TITLE: Resolve_Comment_Import\nFCM: NON-DROP FRAME\n\n")
                print("Writing out EDL file, formating for Resolve's nonsense...")
                print("Parsing TC Values...")
                for i in range(1, sheet.nrows):
                    row = sheet.row_values(i)
                    durations = get_comment_duration(str(row[1]), str(row[2]), fps)
                    contact_tup = (str(row[0]),"  ", "001","      ", "V", "     ", "C", "        ", durations["tc1"],
                                   " ", durations["tc1a"], " ", durations['tc2'], " ", durations["tc2a"], "  ",
                                   "\n |C:ResolveColorBlue |M:", str(row[3]), " |D:", durations['duration_frames'], "\n\n")
                    write_out = "".join(contact_tup)
                    file_out.write(str(write_out))

        except Exception as e:
            print(e)
        print("Success!")
    else:
        print("Enter a valid frame rate: 23.98, 24, 25, 29.97, 30, 50, 59.94, or 60 fps")
        quit()


if __name__ == '__main__':
    fire.Fire(main)

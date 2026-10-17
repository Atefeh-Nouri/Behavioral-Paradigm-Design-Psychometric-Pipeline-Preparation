"""
OpenSesame Practice Feedback Evaluation Script.
Executed in the 'Run' phase of 'feedback_eval'.
Renders immediate trial accuracy feedback and verifies passing threshold.
"""

from openexp.canvas import Canvas

resp_key = var.response
req_key = var.required_key
raw_rt = var.response_time

is_correct = (str(resp_key).lower() == req_key) if resp_key and resp_key != "timeout" else False

# Render immediate visual feedback canvas
feedback_canvas = Canvas(exp)
if is_correct:
    feedback_canvas.text("CORRECT", color="green", font_size=32)
else:
    feedback_canvas.text("INCORRECT", color="red", font_size=32)

feedback_canvas.show()
clock.sleep(exp.vars.config["calibration"]["practice"]["feedback_duration_ms"])

# Track cumulative practice performance
if not hasattr(exp.vars, "practice_correct_count"):
    exp.vars.practice_correct_count = 0
    exp.vars.practice_ax_omissions = 0

if is_correct:
    exp.vars.practice_correct_count += 1
elif var.trial_type == "AX" and (resp_key is None or resp_key == "timeout"):
    exp.vars.practice_ax_omissions += 1

from openedx_caliper_tracking import transformers as ctf

"""
Mapping of events to their transformer functions
"""

EVENT_MAPPING = {
    'edx.bookmark.added': ctf.edx_bookmark_added,
    'edx.bookmark.listed': ctf.edx_bookmark_listed,
    'edx.bookmark.accessed': ctf.edx_bookmark_accessed,
    'edx.bookmark.removed': ctf.edx_bookmark_removed,
    'edx.ui.lms.link_clicked': ctf.edx_ui_lms_link_clicked,
    'edx.course.enrollment.activated': ctf.edx_course_enrollment_activated,
    'edx.course.enrollment.deactivated': ctf.edx_course_enrollment_deactivated,
    'edx.course.enrollment.mode_changed':
        ctf.edx_course_enrollment_mode_changed,
    'edx.course.enrollment.upgrade.clicked':
        ctf.edx_course_enrollment_upgrade_clicked,
    'speed_change_video': ctf.edx_video_speed_changed,
    'edx.course.tool.accessed': ctf.edx_course_tool_accessed,
    'edx.forum.response.created': ctf.edx_forum_response_created,
    'problem_show': ctf.problem_show,
    'edx.ui.lms.sequence.next_selected': ctf.edx_ui_lms_sequence_next_selected,
    'edx.ui.lms.sequence.previous_selected':
        ctf.edx_ui_lms_sequence_previous_selected,
    'seq_next': ctf.seq_next,
    'seq_prev': ctf.seq_prev,
    'stop_video': ctf.stop_video,
    'problem_graded': ctf.problem_graded,
    'problem_save': ctf.problem_save,
    'edx.grades.problem.submitted': ctf.edx_grades_problem_submitted,
    'edx.problem.hint.demandhint_displayed':
        ctf.edx_problem_hint_demandhint_displayed,
    'edx.problem.hint.feedback_displayed':
        ctf.edx_problem_hint_feedback_displayed,
    'pause_video': ctf.pause_video,
    'seek_video': ctf.seek_video,
    'load_video': ctf.load_video,
    'show_transcript': ctf.show_transcript,
    'edx.video.closed_captions.shown': ctf.edx_video_closed_captions_shown,
    'edx.video.closed_captions.hidden': ctf.edx_video_closed_captions_hidden,
    'video_show_cc_menu': ctf.video_show_cc_menu,
    'problem_reset': ctf.problem_reset,
    'seq_goto': ctf.seq_goto,
    'problem_rescore': ctf.problem_rescore,
    'edx.forum.thread.viewed': ctf.edx_forum_thread_viewed,
    'save_problem_success': ctf.save_problem_success,
    'play_video': ctf.play_video,
    'hide_transcript': ctf.hide_transcript,
    'video_hide_cc_menu': ctf.video_hide_cc_menu,
    'edx.forum.thread.created': ctf.edx_forum_thread_created,
    'openassessmentblock.get_peer_submission':
        ctf.openassessmentblock_get_peer_submission,
    'openassessmentblock.peer_assess': ctf.openassessmentblock_peer_assess,
    'edx.course.student_notes.viewed': ctf.edx_course_student_notes_viewed,
    'textbook.pdf.page.navigated': ctf.textbook_pdf_page_navigated,
    'edx.forum.comment.created': ctf.edx_forum_comment_created,
    'xblock.poll.view_results': ctf.xblock_poll_view_results,
    'xblock.survey.view_results': ctf.xblock_survey_view_results,
    'openassessment.student_training_assess_example':
        ctf.openassessment_student_training_assess_example,
    'xblock.survey.submitted': ctf.xblock_survey_submitted,
    'problem_check': ctf.problem_check,
    'openassessmentblock.create_submission':
        ctf.openassessmentblock_create_submission,
    'xblock.poll.submitted': ctf.xblock_poll_submitted,
    'edx.course.student_notes.deleted': ctf.edx_course_student_notes_deleted,
    'edx.course.student_notes.edited': ctf.edx_course_student_notes_edited,
    'edx.course.student_notes.added': ctf.edx_course_student_notes_added,
    'openassessmentblock.get_submission_for_staff_grading':
        ctf.openassessmentblock_get_submission_for_staff_grading,
    'textbook.pdf.page.scrolled': ctf.textbook_pdf_page_scrolled,
    'textbook.pdf.zoom.menu.changed': ctf.textbook_pdf_zoom_menu_changed,
    'textbook.pdf.thumbnail.navigated': ctf.textbook_pdf_thumbnail_navigated,
    'textbook.pdf.zoom.buttons.changed': ctf.textbook_pdf_zoom_buttons_changed,
    'book': ctf.book,
    'edx.course.enrollment.upgrade.succeeded':
        ctf.edx_course_enrollment_upgrade_succeeded,
    'edx.course.student_notes.notes_page_viewed':
        ctf.edx_course_student_notes_notes_page_viewed,
    'edx.cohort.user_added': ctf.edx_cohort_user_added,
    'edx.forum.thread.voted': ctf.edx_forum_thread_voted,
    'edx.forum.response.voted': ctf.edx_forum_response_voted,
    'openassessmentblock.submit_feedback_on_assessments':
        ctf.openassessmentblock_submit_feedback_on_assessments,
    'openassessmentblock.save_submission':
        ctf.openassessmentblock_save_submission,
    'edx.googlecomponent.document.displayed':
        ctf.edx_googlecomponent_document_displayed,
    'edx.googlecomponent.calendar.displayed':
        ctf.edx_googlecomponent_calendar_displayed,
    'openassessmentblock.staff_assess': ctf.openassessmentblock_staff_assess,
    'edx.forum.searched': ctf.edx_forum_searched,
    'oppia.exploration.state.changed': ctf.oppia_exploration_state_changed,
    'textbook.pdf.search.executed': ctf.textbook_pdf_search_executed,
    'openassessmentblock.self_assess': ctf.openassessmentblock_self_assess,
    'edx.drag_and_drop_v2.item.dropped': ctf.edx_drag_and_drop_v2_item_dropped,
    'edx.drag_and_drop_v2.item.picked_up':
        ctf.edx_drag_and_drop_v2_item_picked_up,
    'oppia.exploration.loaded': ctf.oppia_exploration_loaded,
    'ubc.peer_instruction.original_submitted':
        ctf.ubc_peer_instruction_original_submitted,
    'ubc.peer_instruction.revised_submitted':
        ctf.ubc_peer_instruction_revised_submitted,
    'edx.drag_and_drop_v2.loaded': ctf.edx_drag_and_drop_v2_loaded,
    'edx.team.changed': ctf.edx_team_changed,
    'edx.course.home.resume_course.clicked':
        ctf.edx_course_home_resume_course_clicked,
    'edx.special_exam.timed.attempt.created':
        ctf.edx_special_exam_timed_attempt_created,
    'edx.special_exam.timed.attempt.started':
        ctf.edx_special_exam_timed_attempt_started,
    'edx.course.student_notes.used_unit_link':
        ctf.edx_course_student_notes_used_unit_link,
    'edx.special_exam.timed.attempt.submitted':
        ctf.edx_special_exam_timed_attempt_submitted,
    'edx.drag_and_drop_v2.feedback.opened':
        ctf.edx_drag_and_drop_v2_feedback_opened,
    'edx.drag_and_drop_v2.feedback.closed':
        ctf.edx_drag_and_drop_v2_feedback_closed,
    'edx.special_exam.timed.attempt.ready_to_submit':
        ctf.edx_special_exam_time_attempt_ready_to_submit,
    'edx.cohort.created': ctf.edx_cohort_created,
    'edx.special_exam.practice.attempt.created':
        ctf.edx_special_exam_practice_attempt_created,
    'edx.cohort.user_removed': ctf.edx_cohort_user_removed,
    'edx.team.page_viewed': ctf.edx_team_page_viewed,
    'edx.grades.problem.state_deleted': ctf.edx_grades_problem_state_deleted,
    'edx.grades.problem.rescored': ctf.edx_grades_problem_rescored,
    'reset_problem_fail': ctf.reset_problem_fail,
    'edx.grades.problem.score_overridden':
        ctf.edx_grades_problem_score_overridden,
    'edx.team.learner_added': ctf.edx_team_learner_added,
    'reset_problem': ctf.reset_problem,
    'showanswer': ctf.showanswer,
    'edx.special_exam.timed.attempt.deleted':
        ctf.edx_special_exam_timed_attempt_deleted,
    'textbook.pdf.outline.toggled': ctf.textbook_pdf_outline_toggled,
    'oppia.exploration.completed': ctf.oppia_exploration_completed,
    'edx.team.searched': ctf.edx_team_searched,
    'textbook.pdf.search.highlight.toggled':
        ctf.textbook_pdf_search_highlight_toggled,
    'textbook.pdf.searchcasesensitivity.toggled':
        ctf.textbook_pdf_searchcasesensitivity_toggled,
    'edx.course.student_notes.searched': ctf.edx_course_student_notes_searched,
    'edx.user.settings.viewed': ctf.edx_user_settings_viewed,
    'textbook.pdf.thumbnails.toggled': ctf.textbook_pdf_thumbnails_toggled,
    'edx.team.deleted': ctf.edx_team_deleted,
    'edx.team.created': ctf.edx_team_created,
    'ubc.peer_instruction.accessed': ctf.ubc_peer_instruction_accessed,
    'problem_check_fail': ctf.problem_check_fail,
    'textbook.pdf.display.scaled': ctf.textbook_pdf_display_scaled,
    'textbook.pdf.chapter.navigated': ctf.textbook_pdf_chapter_navigated,
    'textbook.pdf.search.navigatednext':
        ctf.textbook_pdf_search_navigatednext,
    'edx.certificate.created': ctf.edx_certificate_created,
    'edx.librarycontentblock.content.removed':
        ctf.edx_librarycontentblock_content_removed,
    'edx.user.settings.changed': ctf.edx_user_settings_changed,
    'xmodule.partitions.assigned_user_to_partition':
        ctf.xmodule_partitions_assigned_user_to_partition,
    'openassessmentblock.save_files_descriptions':
        ctf.openassessmentblock_save_files_descriptions,
    'xblock.split_test.child_render': ctf.xblock_split_test_child_render,
    'edx.librarycontentblock.content.assigned':
        ctf.edx_librarycontentblock_content_assigned,
    'edx.bi.course.upgrade.sidebarupsell.displayed':
        ctf.edx_bi_course_upgrade_sidebarupsell_displayed,
    'save_problem_fail': ctf.save_problem_fail,
    'edx.team.learner_removed': ctf.edx_team_learner_removed,
    'edx.team.activity_updated': ctf.edx_team_activity_updated,
    'edx.special_exam.proctored.created': ctf.edx_special_exam_proctored_created,
    'edx.special_exam.practice.created': ctf.edx_special_exam_practice_created,
    'edx.done.toggled': ctf.edx_done_toggled,
    'edx.special_exam.practice.updated': ctf.edx_special_exam_practice_updated,
    'edx.special_exam.timed.updated': ctf.edx_special_exam_timed_updated,
    'edx.special_exam.proctored.updated': ctf.edx_special_exam_proctored_updated,
    'edx.special_exam.timed.created': ctf.edx_special_exam_timed_created,
    'edx.grades.grading_policy_changed': ctf.edx_grades_grading_policy_changed,
    'page_close': ctf.page_close,
    'edx.certificate.evidence_visited': ctf.edx_certificate_evidence_visited,
    'edx.certificate.shared': ctf.edx_certificate_shared,
    'edx.cohort.creation_requested': ctf.edx_cohort_creation_requested,
    'edx.cohort.user_add_requested': ctf.edx_cohort_user_add_requested,
    'edx.user.login': ctf.edx_user_login,
    'edx.user.logout': ctf.edx_user_logout,
    'edx.course_discovery.search.initiated': ctf.edx_course_discovery_search_initiated,
    'edx.course_discovery.search.results_displayed': ctf.edx_course_discovery_search_results_displayed,
}

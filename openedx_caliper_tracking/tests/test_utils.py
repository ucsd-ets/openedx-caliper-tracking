from smtplib import SMTPException

import mock
from django.test import TestCase, override_settings

from openedx_caliper_tracking import utils
from openedx_caliper_tracking.tests.factories import UserFactory


class CaliperUtilsTestCase(TestCase):

    def test_convert_date_time(self):
        self.assertEquals('2018-10-16T14:23:24.785Z', utils.convert_datetime('2018-10-16T14:23:24.785148+00:00'))

    def test_get_username_from_user_id(self):
        user = UserFactory(username='dummy')
        self.assertEquals('dummy', utils.get_username_from_user_id(user.id))

    @mock.patch(
        'openedx_caliper_tracking.utils.reverse',
        autospec=True,
        return_value='/u/dummy'
    )
    @override_settings(
        LMS_ROOT_URL='https://localhost:18000'
    )
    def test_get_user_link_from_username_without_reverse_not_found_exception(self, reverse_mock):
        formatted_link = utils.get_user_link_from_username('dummy')
        reverse_mock.assert_called_with('learner_profile', kwargs={'username': 'dummy'})
        self.assertEquals('https://localhost:18000/u/dummy', formatted_link)

    @override_settings(
        LMS_ROOT_URL='https://localhost:18000'
    )
    def test_get_user_link_from_username_with_reverse_not_found_exception(self):
        formatted_link = utils.get_user_link_from_username('dummy')
        self.assertEquals('https://localhost:18000/u/dummy', formatted_link)

    def test_get_topic_id_from_team_id(self):
        team_mock = mock.MagicMock()
        with mock.patch.dict('sys.modules', **{
                             'lms': team_mock,
                             'lms.djangoapps': team_mock,
                             'lms.djangoapps.teams': team_mock,
                             'lms.djangoapps.teams.models': team_mock,
                             }):
            utils.get_topic_id_from_team_id(1)
        self.assertEquals(str(team_mock.mock_calls), '[call.CourseTeam.objects.get(team_id=1)]')

    @mock.patch(
        'openedx_caliper_tracking.utils.get_topic_id_from_team_id',
        autospec=True,
        return_value=1
    )
    def test_get_team_url_from_team_id(self, get_topic_id_mock):
        team_url = utils.get_team_url_from_team_id('http://localhost:18000/courses/dummy-course-id/teams/', 1)
        get_topic_id_mock.assert_called_with(1)
        self.assertEquals('http://localhost:18000/courses/dummy-course-id/teams/#teams/1/1', team_url)

    @mock.patch(
        'openedx_caliper_tracking.utils.reverse',
        autospec=True,
        return_value='/certificates/user/8/course/dummy-course-id',
    )
    @override_settings(
        LMS_ROOT_URL='https://localhost:18000'
    )
    def test_get_certificate_url(self, reverse_mock):
        certificate_uri = utils.get_certificate_url(8, 'dummy-course-id')
        self.assertEquals('https://localhost:18000/certificates/user/8/course/dummy-course-id', certificate_uri)
        reverse_mock.assert_called_with('certificates:html_view', kwargs={'user_id': 8, 'course_id': 'dummy-course-id'})

    @mock.patch(
        'openedx_caliper_tracking.utils.log',
        autospec=True,
    )
    @mock.patch(
        'openedx_caliper_tracking.utils.send_mail',
        autospec=True,
        return_value=1
    )
    def test_send_notification_success(self, mail_send_mock, logger_mock):
        data = {
            'name': 'Dummy Support',
            'body': 'Below is the additional information regarding failure:',
            'error': 'dummy error'
        }
        subject = 'Dummy Subject'

        utils.send_notification(data, subject, 'dummy_sender@example.com', ['dummy_receiver@example.com'])
        self.assertTrue(mail_send_mock.called)
        logger_mock.info.assert_called_with('Email has been sent from "dummy_sender@example.com" to '
                                            '"[\'dummy_receiver@example.com\']" for content "{\'body'
                                            '\': \'Below is the additional information regarding '
                                            'failure:\', \'name\': \'Dummy Support\', \'error\': \'dummy error\'}".')

    @mock.patch(
        'openedx_caliper_tracking.utils.log',
        autospec=True,
    )
    @mock.patch(
        'openedx_caliper_tracking.utils.send_mail',
        autospec=True,
        side_effect=SMTPException
    )
    def test_send_notification_failure(self, mail_send_mock, logger_mock):
        data = {
            'name': 'Dummy Support',
            'body': 'Below is the additional information regarding failure:',
            'error': 'dummy error'
        }
        subject = 'Dummy Subject'
        utils.send_notification(data, subject, 'dummy_sender@example.com', ['dummy_receiver@example.com'])
        self.assertTrue(mail_send_mock.called)
        logger_mock.exception.assert_called_with('Unable to send an email from "dummy_sender@example.com" to '
                                                 '"[\'dummy_receiver@example.com\']" for content "{\'body\': '
                                                 '\'Below is the additional information regarding failure:\','
                                                 ' \'name\': \'Dummy Support\', \'error\': \'dummy error\'}".')

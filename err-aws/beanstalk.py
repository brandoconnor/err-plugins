"""
This plugin uses boto3 - ensure that you have a working configuration in order to use this plugin.

http://boto3.readthedocs.org/en/latest/guide/configuration.html
"""
import boto3
from errbot import BotPlugin, botcmd


class Beanstalk(BotPlugin):
    """
    AWS Plugin for checking Elastic Beanstalk environments and more
    """

    @botcmd(split_args_with=None)
    def eb_envs(self, message, args):
        """
        A command which checks Elastic Beanstalk environment statuses for specified
        application environments. If no environment is specified, all are returned.
        """
        if 'eb' not in self:
            self.eb = boto3.client('elasticbeanstalk')

        app_dict = self.eb.describe_applications()
        app_names = []
        for app in app_dict['Applications']:
            app_names.append(app['ApplicationName'])

        # this is done so results are sorted by application
        for app in app_names:
            env_dict = self.eb.describe_environments(ApplicationName=app)
            for env in env_dict['Environments']:
                if args and env['EnvironmentName'] not in args:
                    # Don't report on this environment
                    continue
                yield '{0} - {1}'.format(env['EnvironmentName'], env['Status'])

    @botcmd
    def eb_apps(self, message, args):
        """
        """
        if 'eb' not in self:
            self.eb = boto3.client('elasticbeanstalk')

        apps = self.eb.describe_applications()
        for app in apps['Applications']:
            if args and app['ApplicationName'] not in args:
                continue
            yield '%s - last updated: %s' % (app['ApplicationName'], str(app['DateUpdated']))

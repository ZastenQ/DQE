from TestFramework.configurator import Configurator
from TestFramework.connector import Connector
from TestFramework.processor import Processor
from TestFramework.reporter import Report


def test_run():
    config = Configurator('dev')
    database_url = config.get_database_url()

    connector = Connector(database_url)

    logger = Report()

    processor = Processor(config, connector, logger)
    processor.process()

    logger.finish_test()


if __name__ == '__main__':
    test_run()

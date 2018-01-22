"""
@req: REQ-0004
@req: SOW-FUN-039
@comp: Connectors and Services
@api: developer
"""
import time
from pipeline.classes import AviTask
from connectors.tapquery import AsyncJob

class SASQuery (AviTask):

	def run(self):

		if not hasattr(self, 'query') or not self.query:
			raise Exception(
				"'query' parameter must be provided within pipeline task")

		target = "http://eas.esac.esa.int/tap-dev/tap"
		async_check_interval = 1
		gacs_tap_conn = AsyncJob(target, self.query,
                                 poll_interval=async_check_interval)
		# Run the job (start + wait + raise_exception)
		gacs_tap_conn.run()

		# Store the response
		result = gacs_tap_conn.open_result()
		with open(self.output().path, "wb") as outFile:
			outFile.write(result.content)
		gacs_tap_conn.delete()

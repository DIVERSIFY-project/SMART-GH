# stdlibs
import datetime
import jsonpickle
import logging
import urllib2

# third-party libs

# our libs
import summerlogger

def call_nt_webservice(config_vals):
        logger = \
        logging.getLogger('summer.get_noisetube_readings.call_nt_webservice')
        
        dirname = config_vals['dirname']
        url = config_vals['url']
        api_key = config_vals['api_key']
        city_id = config_vals['city_id']
        data_filename = 'latest_noisetube_readings.json'
        
        full_url = ''.join([url, api_key,'&city=',city_id])
        try:
            logger.info("Webservice at url: %s"%(full_url))
            logger.info("Trying to get data...")
            nt_response = urllib2.urlopen(full_url)
            if nt_response.code == 200:
                logger.info("Data received successfully")
                readings_data = jsonpickle.decode(nt_response.read())
                logger.info("Number of readings received: %s"%(len(readings_data)))
                logger.info("Type of readings_data: %s"%(type(readings_data)))
                full_data_path = ''.join([dirname, data_filename])
                with open(full_data_path, "w") as datafile:
                    datafile.write(jsonpickle.encode(readings_data))
                    logger.info("Finished writing latest NoiseTube data")
        except Exception as e:
            logger.warn("Could not retrieve data from NoiseTube")
            logger.warn("Reason: %s"%(e.str()))
        

if __name__ == '__main__':
    config_vals = {'webservice':'webservices.call_nt_webservice',\
                    'url': 'http://www.noisetube.net/api/search.json?key=',\
                    'api_key': '12da65cd7932fb3a0543009fb78ba08711bed72b',\
                    'city_id': '136', \
                    'dirname': 'sensor_readings/noise/'}

    call_nt_webservice(config_vals)

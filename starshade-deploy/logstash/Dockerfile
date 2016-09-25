FROM logstash:latest
#FROM mongo:latest
# Add your logstash plugins setup here
# Example: RUN logstash-plugin install logstash-filter-json
RUN logstash-plugin install logstash-output-mongodb 
RUN logstash-plugin install logstash-input-beats
RUN logstash-plugin install logstash-input-mongodb 
 

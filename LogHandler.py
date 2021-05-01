class LogHandler:

    def create_new_log(self, file_name):
        log_file = open(file_name + ".txt", 'w+', encoding='utf-8')
        return log_file

    def update_log(self, log_file, log_string):
        log_file.write(log_string + "\n")

    def finalize_log(self, log_file):
        log_file.close()


    def getTransfer(self, actionID, type):
        if type == 'transfer':
            command = 'SELECT srcWellID, dstWellID, Volume, Method FROM Transfers WHERE ExpID = ' + self.expID + ' AND ActionID = ' + str(actionID) + ' ORDER BY trOrder ASC'
        elif type == 'command':
            command = 'SELECT Command, Options, ActionID, trOrder FROM Commands WHERE ExpID = ' + self.expID + ' AND ActionID = ' + str(actionID) + ' ORDER BY trOrder ASC'
        self.crsr.execute(command)
        transferElements = self.crsr.fetchall()
        transfer = {'type' : type, 'info' : []}
        for element in transferElements:
            if type == 'transfer':
                srcWell = self.getWell(element[0])
                dstWell = self.getWell(element[1])
                if self.platform == "tecan":
                    volume = eval(element[2])
                else:
                    volume = element[2]
                method = element[3]
                transfer['info'].append({ 'source' : srcWell, 'destination' : dstWell, 'volume' : volume, 'method' : method })
            if type == 'command':
                if element[0] == 'mix':
                    mixOptions = element[1].split('x')
                    m = self.getAll('SELECT Location FROM CommandLocations WHERE ActionID = ' + str(actionID), order='ORDER BY trOrder ASC')
                    for well in m:
                        w = self.getWell(well)
                        print('mix', mixOptions, element)
                        transfer['info'].append({'command' : 'mix', 'volume' : mixOptions[0], 'times' : mixOptions[1], 'target' : w })
                elif element[0] == 'move':
                    trOrder = element[-1]
                    m = self.getAll('SELECT Location FROM CommandLocations WHERE ActionID = ' + str(actionID) + ' AND trOrder = ' + str(trOrder), order='ORDER BY trOrder ASC')
                    for move in m:
                        transfer['info'].append({'command' : 'move', 'location' : move})
                        
                elif element[0] == 'message' or element[0] == 'comment':
                    command = element[0]
                    message = element[1]
                    transfer['info'].append({'command' : command, 'message' : message})
                
                elif element[0] == 'wait':
                    print('element is wait in the database', element, element[1])
                    wait = element[1]
                    transfer['info'].append({'command' : 'wait', 'wait' : wait})
        return transfer

import multiprocessing as mp
import custom_sched_2
import traceback
import sys
import time


class main_scheduler:

    retry_counter = 0

    def __init__(self,myTr):

        self.myTr = myTr

    def proc_reset(self):

        self.retry_counter = 0

    def start_proc(self, callback, delay, retries):

        print('start_proc called')
        #print('callback: %s' % callback)
        return_pipe_0, feed_pipe_0 = mp.Pipe(duplex=False)
        p = mp.Process(target=self.target_0, args=(feed_pipe_0, return_pipe_0 ))
        p.start()
        feed_pipe_0.send(callback[0])

        try:
            feed_pipe_0.send(callback[1])
        except IndexError:
            #print('no data given')
            feed_pipe_0.send(None)
         
        time.sleep(1)
        
        result = return_pipe_0.recv()

        p.join()
        try:
            if(issubclass(result.__class__, BaseException)):
                self.retry_counter += 1
                self.myTr.logger.error('start_proc(): exception found!')
                print('start_proc(): exception found!')
                self.myTr.logger.error(str(result))
                print(str(result))
                self.myTr.logger.error('in function %s' % callback)
                print('in function %s' % callback)
                self.myTr.logger.error('start_proc(): retry counter: %d' % self.retry_counter)
                print('start_proc(): retry counter: %d' % self.retry_counter)
                if self.retry_counter < retries:
                    time.sleep(delay)
                    result = self.start_proc(callback, delay, retries)
                    print("RETURNING")
                    self.myTr.logger.error('RETURNING')
                    return result
                else:
                    print('to many retries')
                    self.myTr.logger.error('start_proc(): to many retries')
                    return(-1)
            else:
                return result
        except:
            pass
        return result

    def target_0(self, feed_pipe, return_pipe):
        try:
            #execute the callback function
            callback = return_pipe.recv()
            args = return_pipe.recv()
            #if arguments given call with args
            if args:
                #print('args there')
                ret = callback(args)
            else:
                #print('args not there')
                ret = callback()
            #return code
            if ret:
                feed_pipe.send(ret)
            else:
                feed_pipe.send(0)

        except Exception as e:
            print('Exception in target_0(): %s' % sys.exc_info()[0])
            print('Exception in target_0(): %s' % sys.exc_info()[1])
            print('Exception in target_0(): %s' % sys.exc_info()[2])
            print('Exception as e: %s' % e)
            except_type, except_class, tb = sys.exc_info()
            print(type(e))
            #print(issubclass(e.__class__, BaseException))
            #feed_pipe.send((except_type, except_class, traceback.extract_tb(tb)))
            feed_pipe.send(e)

def callback_with_args(args):
    print('callback called with argument: %s' % args)
    # funktioniert nicht, da nur mit einer kopie der
    # Klassen-Instanz gearbeitet wird
    raise ValueError('oha da passt was nicht')
    return 55

def callback_without_args():
    print('callback called without arguments')
    return 77



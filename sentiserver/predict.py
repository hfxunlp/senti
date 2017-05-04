#encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import zmq, sys, json

import seg
import datautils
import spliter

import render_predict

def _predict_core(jsond):
	sock = zmq.Context().socket(zmq.REQ)
	sock.connect("tcp://127.0.0.1:7556")
	sock.send(jsond)
	return sock.recv()

def _predict(srctext):
	seged = datautils.cutParagraph(seg.segline(srctext))
	seqs = datautils.filterChaoes(seged)
	rtaged = datautils.reducebytag(seqs)
	sorted = datautils.sort(set(rtaged.values()))#sorted will be the final model predict input before maped and trans to batches
	splt = spliter.split(sorted)
	batches = datautils.mapBatches(datautils.makeBatches(sorted, splt))
	__pred = json.loads(_predict_core(json.dumps(batches)))
	_pred = []
	for batch in __pred:
		_pred.append(map(list, zip(*batch)))
	p_map = datautils.buildMap(sorted, datautils.mergeBatches(_pred))
	input, pred, sentp = datautils.formatPred(seged, rtaged, p_map)
	return render_predict.render(input, pred, sentp)

def predict(srctext):
	tmp=srctext.strip()
	if tmp:
		return _predict(tmp)
	else:
		return tmp

def poweron():
	seg.poweron()
	datautils.poweron()

def poweroff():
	seg.poweroff()

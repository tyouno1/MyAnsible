#!/usr/bin/python
#coding:utf-8

from ansible.inventory import Inventory
from ansible.playbook import PlayBook
from ansible import callbacks
import ansible.runner
from flask import Flask, request, jsonify, render_template,abort

import commands, json
app = Flask(__name__)

hostfile = '/root/scripts/ansible/inventory/hosts'
'''
  http://127.0.0.1:5000/API/Ansible/playbook?ip=2.2.2.2&playbook=test
  http://192.168.137.101:9001/API/Ansible/playbook?ip=192.168.137.101&playbook=../playbooks/push_key
'''
@app.route('/API/Ansible/playbook')
def Playbook():
    vars={}
    inventory = Inventory(hostfile)
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks()
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats)
    hosts = request.args.get('ip')
    task = request.args.get('playbook')
    vars['hosts'] = hosts
    play=task + '.yaml'
    results = PlayBook(playbook=play, callbacks=playbook_cb,runner_callbacks=runner_cb,
            stats=stats,inventory=inventory,extra_vars=vars)
    res = results.run()
    return json.dumps(res,indent=4)

'''
    curl -H "Content-Type: application/json" -X POST -d '{"ip":"1.1.1.1}",
        "module":"shell","args":"ls -l"}' http://127.0.0.1:5000/API/Ansible/runner
'''
@app.route('/API/Ansible/runner',methods=['POST'])
def Runner():
    print request.json
    if not request.json or not 'ip' in request.json or not 'module' in request.json or not 'args' in request.json:
        abort(400)
    hosts = request.json['ip']
    module = request.json['module']
    args=request.json['args']
    runner = ansible.runner.Runner(module_name = module, module_args=args,
        pattern=hosts, forks=10, host_list=hostfile)
    tasks = runner.run()
    cpis = {}
    cpis1 = {}
    for (hostname, result) in tasks['contacted'].items():
        if not 'failed' in result:
            cpis[hostname] = result['stdout']

    for (hostname, result) in tasks['dark'].items():
        cpis1[hostname] = result['msg']
    return render_template('cpis.html',cpis=cpis,cpis1=cpis1)

@app.route('/')
def index():
    return "test"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)

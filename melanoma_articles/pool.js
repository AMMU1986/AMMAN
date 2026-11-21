'use strict';
// Minimal parallel pool: runs simulation configs across worker threads.
const { Worker, isMainThread, parentPort } = require('worker_threads');
const os = require('os');

if (!isMainThread) {
  const { run } = require('./melanoma_sim');
  parentPort.on('message', ({ id, cfg, reduce }) => {
    const out = run(cfg);
    const red = reduce ? new Function('o', 'cfg', reduce)(out, cfg) : out;
    parentPort.postMessage({ id, red });
  });
} else {
  module.exports = function runAll(cfgs, reduceFn) {
    const nW = Math.min(os.cpus().length, cfgs.length) || 1;
    const reduce = reduceFn ? reduceFn.toString().replace(/^[^{]*{/, '').replace(/}\s*$/, '') : null;
    return new Promise((resolve) => {
      const results = new Array(cfgs.length); let next = 0, done = 0;
      const workers = [];
      for (let w = 0; w < nW; w++) {
        const wk = new Worker(__filename); workers.push(wk);
        wk.on('message', ({ id, red }) => {
          results[id] = red; done++;
          if (next < cfgs.length) { wk.postMessage({ id: next, cfg: cfgs[next], reduce }); next++; }
          if (done === cfgs.length) { workers.forEach(x => x.terminate()); resolve(results); }
        });
        if (next < cfgs.length) { wk.postMessage({ id: next, cfg: cfgs[next], reduce }); next++; }
      }
    });
  };
}

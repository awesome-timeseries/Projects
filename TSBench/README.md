## Supported Platforms
windows 7
Other platforms may work but have not been tested.

## Initial Requirements
Python 2.7

## Usage
### step 1:
<pre><code>
cd NAB
(sudo) pip install -r requirements.txt
</code></pre>

### step 2:
write your own algorithm based on ./tsbench/algorithms/base.py

### step 3:
<pre><code>
python run.py algorithmName proportion scoringMechanism [--delay integer]</pre></code>
If finished successfully, you can find detected results in ./results/

## step 4:
<pre><code>python draw.py</pre></code>
By default, you can open 127.0.0.1/5000/algorithmName/scoringMechanism/ in the brower to see the detected results of your algorithm.

By typing http://127.0.0.1:5000/algorithmName/scoringMechanism/dataPath/, you can see details of the performance on specific time-series data.
eg:
algorithmName = sorad, soring = old dataPath = data/D1/d1-22ta.csv/
http://127.0.0.1:5000/sorad/old/data/D1/d1-22ta.csv/

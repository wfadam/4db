import sys
import numpy
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.preprocessing import normalize
from collections import Counter

hifix = sys.argv[1]

samples = open(hifix).readlines()
n_cols = int(samples[0].split(",")[0])

#m8wX = numpy.loadtxt(hifix,  delimiter=",", usecols=range(2,2 + n_cols))#.reshape(-1, 1)
X = normalize(numpy.loadtxt(hifix,  delimiter=",", usecols=range(2,2 + n_cols)))#.reshape(-1, 1)
MAX_INERTIA = KMeans(n_clusters=1).fit(X).inertia_

N_C_L = 2
N_C_H = 10
nc = N_C_L

inertia_list = []
silhouette_list = []

while nc <= N_C_H:
	km = KMeans(n_clusters=nc).fit(X)
	cluster_labels = km.fit_predict(X)
	silhouette_avg = silhouette_score(X, cluster_labels)

	print ("n_clusters = %d" , nc)

	if(silhouette_avg <= 0.3):
		break

	silhouette_list.append(silhouette_avg)
	inertia_list.append(km.inertia_)

	if(silhouette_avg >= 0.6):
		sample_silhouette_values = silhouette_samples(X, cluster_labels)
		n_samp_in_cluster = Counter(cluster_labels)

		for idx, cls in enumerate(km.cluster_centers_):
			print ("\tCenter of cluster%d : %s" , idx, " ".join([str("%.4f"%e) for e in cls]))

		for n_label in range(0, nc):
			cnt = n_samp_in_cluster[n_label]
			print ("\tSize of cluster%d : %d" , n_label, cnt)
			if(cnt <= 11):
				str_list = []
				for label, silh, line in zip(cluster_labels, sample_silhouette_values, samples):
					if(label == n_label):
						str_list.append("\t%.2f, %s" % (silh, line.strip()))
				print ("\n".join(sorted(str_list)))

	nc = nc + 1

print ("=" * 40)
print ("nc\tnorm\tinertia\tsilhouette")
nc = N_C_L
for inertia, silhouette in zip(inertia_list, silhouette_list):
	print ("%2d\t%.3f\t%7.0f\t%10.2f" , nc, inertia/MAX_INERTIA, inertia, silhouette)
	nc = nc + 1



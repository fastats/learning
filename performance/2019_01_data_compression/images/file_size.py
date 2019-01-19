import matplotlib.pyplot as plt

data = {
    'initial': 268,
    'ident_category': 248,
    'float32': 212,
    'date_category': 158,
}

categorical_compression = {
    'initial': 268,
    'cat': 194,
    'initial_comp': 187,
    'cat_comp': 29
}

compression_size = {
    'uncompressed': 158,
    'hdf5: zlib9': 22,
    'hdf5: blosc:zstd': 19,
    'parquet: default': 7
}


# xticks = []
# for idx, (key, value) in enumerate(data.items()):
#     plt.bar(idx, value, width=0.35, label=key)
#     xticks.append(key)
#
# plt.xticks((0, 1, 2, 3), xticks)
# plt.xlabel('File size')
# plt.ylabel('Size (Mb)')
# plt.show()

plt.bar((0, 1), (268, 187), width=0.35, label='Initial')
plt.bar((0.35, 1.35), (194, 29), width=0.35, label='Categorical')
plt.legend(loc='upper right')
plt.xticks((0.17, 1.17), ('Uncompressed', 'Compressed'))
plt.xlabel('Data Type')
plt.ylabel('File Size (Mb)')
plt.show()

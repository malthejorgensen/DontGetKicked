# The list is needed for order (the order of the columns)
# Because dictionary traversal order is not well-defined
# (maybe it is in Python but we can't rely on it)
colnames = ['RefId', 'IsBadBuy', 'PurchDate', 'Auction', 'VehYear', 'VehicleAge', 'Make',  'Model', 'Trim',  'SubModel', 'Color', 'Transmission', 'WheelTypeID', 'WheelType', 'VehOdo', 'Nationality', 'Size',  'TopThreeAmericanName', 'MMRAcquisitionAuctionAveragePrice', 'MMRAcquisitionAuctionCleanPrice', 'MMRAcquisitionRetailAveragePrice', 'MMRAcquisitonRetailCleanPrice', 'MMRCurrentAuctionAveragePrice', 'MMRCurrentAuctionCleanPrice', 'MMRCurrentRetailAveragePrice', 'MMRCurrentRetailCleanPrice', 'PRIMEUNIT', 'AUCGUART', 'BYRNO', 'VNZIP1', 'VNST',  'VehBCost', 'IsOnlineSale', 'WarrantyCost']


data_options = {
 'RefId': ('int32', 'Skip'),
 'IsBadBuy': ('i1', 'Skip'),
 'PurchDate': ('int64', 5),
 'Auction': ('S10', 10),
 'VehYear': ('int64', 10),
 'VehicleAge': ('int32', 5),
 'Make': ('S10', 5),
 'Model': ('S10', 5),
 'Trim': ('S10', 5),
 'SubModel': ('S10', 5),
 'Color': ('S10', 'Skip'),
 'Transmission': ('S10', 5),
 'WheelTypeID': ('int32', 'Skip'),
 'WheelType': ('S10', 5),
 'VehOdo': ('int32', 5), 
 'Nationality': ('S10', 5),
 'Size': ('S10', 5),
 'TopThreeAmericanName': ('S10', 5),
 'MMRAcquisitionAuctionAveragePrice': ('int32', 'Skip'),
 'MMRAcquisitionAuctionCleanPrice': ('int32', 'Skip'),
 'MMRAcquisitionRetailAveragePrice': ('int32', 'Skip'),
 'MMRAcquisitonRetailCleanPrice': ('int32', 'Skip'),
 'MMRCurrentAuctionAveragePrice': ('int32', 'Skip'),
 'MMRCurrentAuctionCleanPrice': ('int32', 'Skip'),
 'MMRCurrentRetailAveragePrice': ('int32', 'Skip'),
 'MMRCurrentRetailCleanPrice': ('int32', 'Skip'), 
 'PRIMEUNIT': ('S10', 'Skip'),
 'AUCGUART': ('S10', 'Skip'), 
 'BYRNO': ('int32', 'Skip'),
 'VNZIP1': ('int32', 10),
 'VNST': ('S10', 10),
 'VehBCost': ('int32', 5),
 'IsOnlineSale': ('S10', 3),
 'WarrantyCost': ('int32', 7),
 }

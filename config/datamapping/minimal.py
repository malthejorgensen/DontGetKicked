# The list is needed for order (the order of the columns)
# Because dictionary traversal order is not well-defined
# (maybe it is in Python but we can't rely on it)
colnames = ['RefId', 'IsBadBuy', 'PurchDate', 'Auction', 'VehYear', 'VehicleAge', 'Make',  'Model', 'Trim',  'SubModel', 'Color', 'Transmission', 'WheelTypeID', 'WheelType', 'VehOdo', 'Nationality', 'Size',  'TopThreeAmericanName', 'MMRAcquisitionAuctionAveragePrice', 'MMRAcquisitionAuctionCleanPrice', 'MMRAcquisitionRetailAveragePrice', 'MMRAcquisitonRetailCleanPrice', 'MMRCurrentAuctionAveragePrice', 'MMRCurrentAuctionCleanPrice', 'MMRCurrentRetailAveragePrice', 'MMRCurrentRetailCleanPrice', 'PRIMEUNIT', 'AUCGUART', 'BYRNO', 'VNZIP1', 'VNST',  'VehBCost', 'IsOnlineSale', 'WarrantyCost']


data_options = {
 'RefId': ('int32', 'Skip'),
 'IsBadBuy': ('i1', 'Skip'),
 'PurchDate': ('int64', 'Skip'),
 'Auction': ('S10', 'Skip'),
 'VehYear': ('int64', 'Skip'),
 'VehicleAge': ('int32', 'Skip'),
 'Make': ('S10', 'Skip'),
 'Model': ('S10', 'Skip'),
 'Trim': ('S10', 'Skip'),
 'SubModel': ('S10', 'Skip'),
 'Color': ('S10', 'Skip'),
 'Transmission': ('S10', 'Skip'),
 'WheelTypeID': ('int32', 'Skip'),
 'WheelType': ('S10', 'Skip'),
 'VehOdo': ('int32', 'Skip'), 
 'Nationality': ('S10', 'Skip'),
 'Size': ('S10', 'Skip'),
 'TopThreeAmericanName': ('S10', 'Skip'),
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
 'VNZIP1': ('int32', 'Skip'),
 'VNST': ('S10', 'Skip'),
 'VehBCost': ('int32', 'Skip'),
 'IsOnlineSale': ('S10', 'All'),
 'WarrantyCost': ('int32', 'Skip'),
 }

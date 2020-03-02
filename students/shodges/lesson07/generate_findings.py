"""
Run linear and parallel imports and provide time data.
"""
import datetime
import linear
import parallel

linear.drop_data()

print("--- Running linear import ---")
start_time = datetime.datetime.now()
results = linear.import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')
print("Products:")
print("   Records: {} processed, {} imported".format(results[0][0], results[0][2] - results[0][1]))
print("   Runtime: {} seconds".format(results[0][3]))
print()
print("Customers:")
print("   Records: {} processed, {} imported".format(results[1][0], results[1][2] - results[1][1]))
print("   Runtime: {} seconds".format(results[1][3]))
print()
print("Linear import complete in {} seconds.".format(
      (datetime.datetime.now() - start_time).total_seconds()))
print()

parallel.drop_data()

print("--- Running parallel import ---")
start_time = datetime.datetime.now()
results = parallel.import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')
print("Products:")
print("   Records: {} processed, {} imported".format(results[0][0], results[0][2] - results[0][1]))
print("   Runtime: {} seconds".format(results[0][3]))
print()
print("Customers:")
print("   Records: {} processed, {} imported".format(results[1][0], results[1][2] - results[1][1]))
print("   Runtime: {} seconds".format(results[1][3]))
print()
print("Parallel import complete in {} seconds.".format(
      (datetime.datetime.now() - start_time).total_seconds()))

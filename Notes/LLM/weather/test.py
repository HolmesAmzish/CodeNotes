import asyncio
import weather

result = asyncio.run(weather.get_alerts("TX"))
print(result)
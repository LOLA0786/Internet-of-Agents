import time
from producer_agent import ProducerAgent
from trader_agent import TraderAgent
from consumer_agent import ConsumerAgent

if __name__ == "__main__":
    print("Launching AgentNet: Internet of Agents Prototype")
    print("Agents will collaborate to trade data and hit a shared goal score >80.\n")

    # Init agents on different ports (local network sim)
    producer = ProducerAgent(5000)
    trader = TraderAgent(5001)
    consumer = ConsumerAgent(5002)

    # Start all
    producer.start()
    trader.start()
    consumer.start()

    try:
        # Run sim for 30s (or until goal hit)
        time.sleep(30)
    except KeyboardInterrupt:
        print("\nStopping agents...")
    finally:
        producer.running = trader.running = consumer.running = False
        print("Demo complete! Check GitHub for expansions (e.g., real MCP).")

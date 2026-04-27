from langchain_core.output_parsers import PydanticOutputParser
from model import ActionItemsOutput


parser = PydanticOutputParser(pydantic_object=ActionItemsOutput)
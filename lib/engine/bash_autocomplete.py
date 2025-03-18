
SUGGESTION_CODE_TARGET_OPTION = 0
SUGGESTION_CODE_PATH = 1



def output_suggestions(suggestions):
	print(SUGGESTION_CODE_TARGET_OPTION)
	print("\n".join(sorted(suggestions)))
